import threading
from flask import Blueprint, request, jsonify
import json
import os
import base64
import ffmpeg
from sqlalchemy import func
from werkzeug.utils import secure_filename
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from src.modules.realtime_conversation import InterviewBot
from src.modules.post_conversation import PostConversationProcessor
from src.modules.interview_q_a import InterviewQA
from src.db.user import User
from src.db.qa import QA
from src.db.interview_record import InterviewRecord
from src.utils.extensions import db
from src.tools.fast_transfer import transfer
from src.tools.speech_synthesis import run_tts
from transformers import BertTokenizer, BertForSequenceClassification
from src.utils.now_sentiment import RealTimeEmotionAnalyzer
from src.modules import ConversationVerifier

relate_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

interview_bp = Blueprint('interview', __name__, url_prefix='/api/interview')

UPLOAD_RESUME_FOLDER = os.path.join(relate_path, 'data/cvs')
os.makedirs(UPLOAD_RESUME_FOLDER, exist_ok=True)

FRAME_PATH = os.path.join(relate_path, 'data/frame')
os.makedirs(FRAME_PATH, exist_ok=True)

model_path = os.path.join(relate_path, r'model/roberta-jd')
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)


# 线程安全的全局状态管理
class ThreadSafeInterviewManager:
    def __init__(self):
        self._lock = threading.RLock()
        self._user_states = {}
        self._thread_pool = ThreadPoolExecutor(max_workers=10)

    def get_user_state(self, user_id):
        with self._lock:
            if user_id not in self._user_states:
                self._user_states[user_id] = {
                    'choose_type': 'hr',
                    'choose_level': 'mild',
                    'bot': None,
                    'processor': None,
                    'analyzer': None,
                    'vcn': 'x4_yezi',
                    'questions': ["你好，请先开始自我介绍"],
                    'answers': [],
                    'feedbacks': [],
                    'state_lock': threading.RLock()
                }
            return self._user_states[user_id]

    def update_user_state(self, user_id, key, value):
        user_state = self.get_user_state(user_id)
        with user_state['state_lock']:
            user_state[key] = value

    def get_user_value(self, user_id, key):
        user_state = self.get_user_state(user_id)
        with user_state['state_lock']:
            return user_state.get(key)

    def append_to_user_list(self, user_id, list_key, value):
        user_state = self.get_user_state(user_id)
        with user_state['state_lock']:
            if list_key not in user_state:
                user_state[list_key] = []
            user_state[list_key].append(value)

    def clear_user_list(self, user_id, list_key):
        user_state = self.get_user_state(user_id)
        with user_state['state_lock']:
            if list_key in user_state:
                user_state[list_key].clear()

    def get_user_list_length(self, user_id, list_key):
        user_state = self.get_user_state(user_id)
        with user_state['state_lock']:
            return len(user_state.get(list_key, []))

    def get_user_list_item(self, user_id, list_key, index):
        user_state = self.get_user_state(user_id)
        with user_state['state_lock']:
            user_list = user_state.get(list_key, [])
            if 0 <= index < len(user_list):
                return user_list[index]
            return None

    def submit_task(self, func, *args, **kwargs):
        return self._thread_pool.submit(func, *args, **kwargs)

    def cleanup_user_state(self, user_id):
        with self._lock:
            if user_id in self._user_states:
                del self._user_states[user_id]


# 全局管理器实例
manager = ThreadSafeInterviewManager()


def convert_webm_to_mp4(input_path):
    """线程安全的视频转换函数"""
    output_path = input_path[:-5] + '.mp4'

    # 添加文件锁机制
    lock_file = input_path + '.lock'

    try:
        # 检查锁文件是否存在
        if os.path.exists(lock_file):
            return False

        # 创建锁文件
        with open(lock_file, 'w') as f:
            f.write(str(os.getpid()))

        (
            ffmpeg
            .input(input_path)
            .output(output_path, r=25, s='1280x720', vcodec='libx264', acodec='aac')
            .run(overwrite_output=True)
        )

        if os.path.exists(input_path):
            os.remove(input_path)

        return True

    except Exception as e:
        print(f"Video conversion error: {e}")
        return False
    finally:
        # 清理锁文件
        if os.path.exists(lock_file):
            os.remove(lock_file)


@interview_bp.route('/type', methods=['POST'])
def interview_type():
    data = request.json
    interview_type = data.get('type')
    username = data.get('username')
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    manager.update_user_state(user.id, 'choose_type', interview_type)
    print(f"User {user.id} set interview type: {interview_type}")

    return jsonify({'message': 'success', 'data': interview_type})


@interview_bp.route('/level', methods=['POST'])
def interview_level():
    data = request.json
    level = data.get('level')
    username = data.get('username')
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    manager.update_user_state(user.id, 'choose_level', level)
    print(f"User {user.id} set interview level: {level}")

    return jsonify({'message': 'success', 'data': level})


@interview_bp.route('/init-bot', methods=['POST'])
def init_bot():
    data = request.json
    username = data.get('username')
    scene = data.get('scene')

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if not user.resume_name:
        return jsonify({'error': '请上传简历'}), 404

    cv_path = os.path.join(UPLOAD_RESUME_FOLDER, user.resume_name)

    # 重置用户状态
    manager.clear_user_list(user.id, 'questions')
    manager.clear_user_list(user.id, 'answers')
    manager.clear_user_list(user.id, 'feedbacks')
    manager.append_to_user_list(user.id, 'questions', "你好，请先开始自我介绍")
    manager.update_user_state(user.id, 'processor', None)

    # 获取用户设置
    choose_type = manager.get_user_value(user.id, 'choose_type')
    choose_level = manager.get_user_value(user.id, 'choose_level')

    bot = InterviewBot(
        cv_path=cv_path,
        name=user.realname,
        interviewer_type=choose_type,
        job_role=user.job_position,
        candidate_skill=choose_level,
        role_description=user.job_requirement,
        scene=scene,
    )

    manager.update_user_state(user.id, 'bot', bot)

    return jsonify({'message': 'success'})


@interview_bp.route('/chart', methods=['POST'])
def interview_chart():
    data = request.json
    text = data.get('text')
    username = data.get('username')
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    bot = manager.get_user_value(user.id, 'bot')
    if not bot:
        return jsonify({'error': 'Bot not initialized'}), 400

    manager.append_to_user_list(user.id, 'answers', text)

    response, _, _ = bot.main(text)
    manager.append_to_user_list(user.id, 'questions', response)

    return jsonify({'message': 'success', 'reply': response})


@interview_bp.route('/text-analyze', methods=['POST'])
def text_analyze():
    data = request.json
    username = data.get('username')
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    questions_len = manager.get_user_list_length(user.id, 'questions')
    answers_len = manager.get_user_list_length(user.id, 'answers')

    if answers_len > 0 and questions_len > answers_len:
        question = manager.get_user_list_item(user.id, 'questions', answers_len - 1)
        answer = manager.get_user_list_item(user.id, 'answers', answers_len - 1)
        dialog_analyze(user.id, question, answer)

    return jsonify({'message': 'success'})


@interview_bp.route('/text-report/<username>', methods=['POST'])
def text_report(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if not user.resume_name:
        return jsonify({'error': '请上传简历'}), 404

    bot = manager.get_user_value(user.id, 'bot')
    if not bot:
        return jsonify({'error': 'Bot not initialized'}), 400

    # 获取建议
    path = os.path.join(relate_path, f"data/cvs/{user.resume_name[:-11]}-feedback.json")
    if not os.path.exists(path):
        advice = ""
    else:
        with open(path, 'r', encoding='utf-8') as file:
            advice = json.load(file)

    # 创建处理器
    processor = PostConversationProcessor(bot.path_name, 0.47, model, tokenizer)
    manager.update_user_state(user.id, 'processor', processor)

    feedbacks = manager.get_user_value(user.id, 'feedbacks')
    processor.end_sentiments(feedbacks, advice, "text")

    # 读取结果
    outcome_path = os.path.join(relate_path, f"data/interviews/{processor.path_name}/outcome/")
    with open(outcome_path + "evaluation.json", 'r', encoding='utf-8') as file:
        evaluation = json.load(file)
    with open(outcome_path + "chatlog.json", 'r', encoding='utf-8') as file:
        chatlog = json.load(file)

    # 保存到数据库
    interview_record = InterviewRecord(
        user_id=user.id,
        interview_type=bot.interviewer_type,
        candidate_skill=bot.candidate_skill,
        job_role=bot.job_role,
        role_description=bot.role_description,
        time=bot.time,
        scene=bot.scene,
        chatlog=chatlog if chatlog else None,
        evaluation=evaluation if evaluation else None,
    )
    db.session.add(interview_record)
    db.session.commit()

    return jsonify({'evaluation': evaluation, 'chatlog': chatlog})


@interview_bp.route('/video-chart/<username>', methods=['POST'])
def upload_audio(username):
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file in request'}), 400

    file = request.files['audio']
    filename = secure_filename(file.filename)
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    bot = manager.get_user_value(user.id, 'bot')
    if not bot:
        return jsonify({'error': 'Bot not initialized'}), 400

    # 生成唯一的文件名避免冲突
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    unique_filename = f"{user.id}_{timestamp}_{filename}"
    audio_path = os.path.join(bot.audio_directory, unique_filename[:-4] + '-active.wav')

    file.save(audio_path)

    result = transfer(audio_path)
    if result is None:
        return jsonify({'error': 'Failed to transfer audio'}), 400

    manager.append_to_user_list(user.id, 'answers', result)

    text_path = os.path.join(bot.text_directory, unique_filename[:-4] + '-active.txt')
    with open(text_path, 'w', encoding='utf-8') as file:
        file.write(result)

    response, _, _ = bot.main(result)
    manager.append_to_user_list(user.id, 'questions', response)

    # 生成语音
    speech_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    speech_name = f"recording_{user.id}_{speech_timestamp}.mp3"
    speech_path = os.path.join(bot.speech_directory, speech_name)

    vcn = manager.get_user_value(user.id, 'vcn')
    run_tts(speech_path, response, vcn)

    return jsonify({'message': 'Audio uploaded successfully', 'text': response, "file": speech_name})


@interview_bp.route('/update-vcn', methods=['POST'])
def update_vcn():
    data = request.json
    interview_vcn = data.get('vcn')
    username = data.get('username')
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if interview_vcn:
        manager.update_user_state(user.id, 'vcn', interview_vcn)
        return jsonify({'message': 'VCN updated successfully', 'vcn': interview_vcn})
    else:
        return jsonify({'error': 'VCN not provided'}), 400


@interview_bp.route('/get-audio-base64', methods=['POST'])
def get_audio_base64():
    data = request.json
    filename = data.get('filename')
    username = data.get('username')
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    bot = manager.get_user_value(user.id, 'bot')
    if not bot:
        return jsonify({'error': 'Bot not initialized'}), 400

    filepath = os.path.join(bot.speech_directory, filename)

    try:
        with open(filepath, 'rb') as f:
            encoded = base64.b64encode(f.read()).decode('utf-8')
        return jsonify({'base64_audio': encoded})
    except FileNotFoundError:
        return jsonify({'error': 'Audio file not found'}), 404


@interview_bp.route('/upload-media/<username>', methods=['POST'])
def upload_media(username):
    if 'media' not in request.files:
        return jsonify({'error': 'No media file in request'}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    bot = manager.get_user_value(user.id, 'bot')
    if not bot:
        return jsonify({'error': 'Bot not initialized'}), 400

    file = request.files['media']
    filename = secure_filename(file.filename)

    # 生成唯一文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    unique_filename = f"{user.id}_{timestamp}_{filename}"
    save_path = os.path.join(bot.video_directory, unique_filename[:-5] + '-active.webm')

    file.save(save_path)

    # 异步转换视频
    future = manager.submit_task(convert_webm_to_mp4, save_path)

    return jsonify({'message': 'File uploaded successfully', 'filename': unique_filename})


def dialog_analyze(user_id, question, answer):
    """异步对话分析"""
    temp_dict = {
        'interviewer': question,
        'candidate': answer
    }
    print(f"User {user_id} temp_dict: ", temp_dict)

    feedback = ConversationVerifier.process_qa_pair(temp_dict)
    print(f"User {user_id} feedback: ", feedback)

    manager.append_to_user_list(user_id, 'feedbacks', feedback)


def sentiment_analyze(user_id):
    """异步情感分析"""
    processor = manager.get_user_value(user_id, 'processor')
    bot = manager.get_user_value(user_id, 'bot')

    if processor is None:
        processor = PostConversationProcessor(bot.path_name, 0.47, model, tokenizer)
        manager.update_user_state(user_id, 'processor', processor)

    processor.handle_sentiments()


@interview_bp.route('/handle_sentiments/<username>', methods=['POST'])
def handle_sentiments(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    questions_len = manager.get_user_list_length(user.id, 'questions')
    answers_len = manager.get_user_list_length(user.id, 'answers')

    if answers_len > 0 and questions_len > answers_len:
        question = manager.get_user_list_item(user.id, 'questions', answers_len - 1)
        answer = manager.get_user_list_item(user.id, 'answers', answers_len - 1)

        sentiment_analyze(user.id),
        dialog_analyze(user.id, question, answer)

    return jsonify({"message": "success"})


def end_emotion(user_id):
    """获取情感分析结果"""
    bot = manager.get_user_value(user_id, 'bot')
    if not bot:
        return None

    path = os.path.join(relate_path, 'data/interviews', bot.path_name, 'emotion_time_series/emotion.json')
    if not os.path.exists(path):
        return None

    try:
        with open(path, 'r', encoding='utf-8') as file:
            emotions = json.load(file)
        return emotions
    except Exception as e:
        print(f"Error reading emotion file: {e}")
        return None


def end_evaluation(user_id):
    """生成最终评估"""
    user = User.query.filter_by(id=user_id).first()
    if not user or not user.resume_name:
        return None, None

    bot = manager.get_user_value(user_id, 'bot')
    processor = manager.get_user_value(user_id, 'processor')

    if not bot or not processor:
        return None, None

    path = os.path.join(relate_path, f"data/cvs/{user.resume_name[:-11]}-feedback.json")
    if not os.path.exists(path):
        advice = ""
    else:
        with open(path, 'r', encoding='utf-8') as file:
            advice = json.load(file)

    feedbacks = manager.get_user_value(user_id, 'feedbacks')
    processor.end_sentiments(feedbacks, advice, "video")

    outcome_path = os.path.join(relate_path, f"data/interviews/{processor.path_name}/outcome/")

    try:
        with open(outcome_path + "evaluation.json", 'r', encoding='utf-8') as file:
            evaluation = json.load(file)
        with open(outcome_path + "chatlog.json", 'r', encoding='utf-8') as file:
            chatlog = json.load(file)
        return evaluation, chatlog
    except Exception as e:
        print(f"Error reading evaluation files: {e}")
        return None, None


@interview_bp.route('/end_sentiments/<username>', methods=['POST'])
def end_sentiments(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    bot = manager.get_user_value(user.id, 'bot')
    if not bot:
        return jsonify({'error': 'Bot not initialized'}), 400

    evaluation, chatlog = end_evaluation(user.id)
    emotions, = end_emotion(user.id),

    if evaluation:
        interview_record = InterviewRecord(
            user_id=user.id,
            interview_type=bot.interviewer_type,
            candidate_skill=bot.candidate_skill,
            job_role=bot.job_role,
            role_description=bot.role_description,
            time=bot.time,
            scene=bot.scene,
            chatlog=chatlog if chatlog else None,
            evaluation=evaluation if evaluation else None,
            emotions=emotions if emotions else None,
        )
        db.session.add(interview_record)
        db.session.commit()

    # 清理用户状态
    manager.cleanup_user_state(user.id)

    response_data = {'evaluation': evaluation} if evaluation else {'error': 'Failed to generate evaluation'}
    if emotions:
        response_data['emotions'] = emotions
    if chatlog:
        response_data['chatlog'] = chatlog

    return jsonify(response_data)


def generate_qa(username, position=None, level=None):
    """生成问答稿"""
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if not user.resume_name:
        return jsonify({'error': '生成问答稿失败，请先上传简历'}), 404

    cv_path = os.path.join(relate_path, 'data/cvs', user.resume_name)
    job_role = position if position else user.job_position
    candidate_skill = level if level else "初级"
    role_description = ""

    print(f"job_role: {job_role}")
    print(f"candidate_skill: {candidate_skill}")

    qa_bot = InterviewQA(
        cv_path=cv_path,
        job_role=job_role,
        candidate_skill=candidate_skill,
        role_description=role_description,
        username=user.realname,
    )

    response = qa_bot.run()

    if not response:
        return jsonify({'error': '生成问答稿失败，请重新生成'}), 404

    qa = QA(
        job_role=job_role,
        candidate_skill=candidate_skill,
        role_description=role_description,
        questions=response,
        time=datetime.now(),
        user_id=user.id
    )
    db.session.add(qa)
    db.session.commit()

    return jsonify(response)


@interview_bp.route('/get-qa/<username>', methods=['POST'])
def get_qa(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    qa = QA.query.filter_by(user_id=user.id).all()

    if not qa:
        return generate_qa(username)
    else:
        data = qa[-1].questions
        return jsonify(data)


@interview_bp.route('/update-qa', methods=['POST'])
def update_qa():
    data = request.json
    username = data.get('username')
    position = data.get('position')
    level = data.get('level')

    return generate_qa(username, position, level)


@interview_bp.route('/fetch-frame/<time>/<username>', methods=['POST'])
def fetch_frame(time, username):
    frame = request.files.get('frame')
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    analyzer = manager.get_user_value(user.id, 'analyzer')
    if not analyzer:
        analyzer = RealTimeEmotionAnalyzer()
        manager.update_user_state(user.id, 'analyzer', analyzer)

    if frame:
        # 生成唯一文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{user.id}_{timestamp}_{secure_filename(frame.filename)}"
        emotion_path = os.path.join(FRAME_PATH, filename)

        try:
            frame.save(emotion_path)
            data = analyzer.update_with_frame(emotion_path, float(time))
            return jsonify(data)
        except Exception as e:
            print(f"Error processing frame: {e}")
            return jsonify({'error': 'Failed to process frame'}), 500
        finally:
            if os.path.exists(emotion_path):
                os.remove(emotion_path)

    return jsonify({'error': 'No frame provided'}), 400


@interview_bp.route('/get-history/<username>', methods=['POST'])
def get_history(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    interviews = InterviewRecord.query.filter_by(user_id=user.id).all()

    history = []
    for interview in interviews:
        if interview.evaluation:
            history.append({
                'fullReport': interview.evaluation,
                'date': interview.time.strftime('%Y-%m-%d %H:%M:%S'),
                'scene': interview.scene,
                'type': interview.interview_type,
                'level': interview.candidate_skill,
                'job_role': interview.job_role,
                'chatlog': interview.chatlog if interview.chatlog else None,
            })

    return jsonify(history)

@interview_bp.route('get-interview-count', methods=['POST'])
def get_interview_count():
    data = request.json
    username = data.get('username')
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    text_count = InterviewRecord.query.filter_by(user_id=user.id, scene='text').count()
    audio_count = InterviewRecord.query.filter_by(user_id=user.id, scene='audio').count()
    video_count = InterviewRecord.query.filter_by(user_id=user.id, scene='video').count()
    qa_count = QA.query.filter_by(user_id=user.id).count()
    return jsonify({'text': text_count, 'audio': audio_count, 'video': video_count, 'qa': qa_count})

@interview_bp.route('get-interview-top-list', methods=['POST'])
def get_interview_top_list():
    users_query = (
        db.session.query(
            InterviewRecord.user_id,
            func.count(InterviewRecord.id).label('record_count')
        )
        .group_by(InterviewRecord.user_id)
        .order_by(func.count(InterviewRecord.id).desc())
        .limit(10)
        .all()
    )

    # 转换为字典列表
    top_list = [
        {
            'username': User.query.filter_by(id=row.user_id).first().username,
            'interviewCount': row.record_count,
            'location': User.query.filter_by(id=row.user_id).first().location if User.query.filter_by(id=row.user_id).first().location else '未知',
            'university': User.query.filter_by(id=row.user_id).first().university if User.query.filter_by(id=row.user_id).first().university else '未知学校',
            'isHot': index < 3,
        }
        for index, row in enumerate(users_query)
    ]

    return jsonify(top_list)