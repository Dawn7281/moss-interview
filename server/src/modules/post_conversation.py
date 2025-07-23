import os
from dotenv import load_dotenv
from joblib import load
# from src.utils.xfyun_chat import XFYunChat
# from src.utils.humewrapper import HumeSentimentAnalyzer
from src.utils.xfyun_chat import XFYunChat
# from src.utils.humewrapper import HumeSentimentAnalyzer
from src.modules import ConversationVerifier
import traceback
import json
from src.utils.sentime_analyse_new import generate_feedback, load_local_model
from transformers import BertTokenizer, BertForSequenceClassification
from src.modules.resume_optimizer import *
from src.utils.sentime_analyse_new import extract_emotion_series
from fer import FER

relate_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# 音频模型加载
save_dir = os.path.join(relate_path, r"model/chinese_emotion_model") # 本地模型目录
extractor, audio_model, classifier, config = load_local_model(save_dir)

# 初始化 FER 检测器
detector = FER(mtcnn=True)

class PostConversationProcessor:
    """Processes post-conversation data for candidate evaluation."""
    def __init__(self, path_name, pass_rate,model,tokenizer):
        """
        Initialize the PostConversationProcessor.

        Args:
            timestamp (str): Timestamp of the interview.
        """
        load_dotenv(os.path.join(os.path.dirname(os.getcwd()), ".env"))
        # self.timestamp = timestamp
        self.path_name = path_name
        self.pass_rate = str(pass_rate)
        interview_path = os.path.join(relate_path, 'data/interviews/')
        self.directory = os.path.join(interview_path, self.path_name)
        self.chatlog = load(os.path.join(self.directory, "joblib/conversation.joblib"))
        self.setup_models()
        self.sentiments = []
        self.output_files = []
        self.start_video_time = 0.0

        self.model = model
        self.tokenizer = tokenizer

    def setup_models(self):
        load_dotenv()
        """Set up the sentiment analyzer and AI models."""
        try:
            print('hume_apikey:',os.getenv("HUME_API_KEY"))
            # self.sentiment_analyser = HumeSentimentAnalyzer(api_key=os.getenv("HUME_API_KEY"))
            
            sentiment_system_prompt = """You are a skilled emotions analyst provided with a detailed breakdown of sentiment analysis scores from Hume.ai, for a single response in an interview to a question from the interviewer. The scores are split into 3 sections. All numbers are from 0 to 1, linearly scaling, with 1 being a very strong representation of the indicator in question.

            First, Emotions. This contains several human emotions with a numerical value indicating the strength of the corresponding emotion.
            Second, Sentiments. This contains a scale from 1 to 9, each containing a numerical value indicating the magnitude of the sentiment of the topic of the conversation. A negative topic such as murder will have a high value lower in the scale, such as 1 or 2, and a positive topic will have a high value from 0 to 1 higher in the scale such as 8 or 9.
            Third, Toxicity. This contains several toxic representations such as hate, insult, etc, with a value from 0 to 1 for each representation identified in the audio.

            Your job is to provide a concise detailed one sentence breakdown of how the individual was feeling for the particular scores provided. You must be highly objective as your job is to discern whether or not a candidate was exhibiting traits which would or would not be fitting for a successful interview. 
            Model your answer beginning with something along the lines of "For this particular response, the candidate...
            Your output must be in Chinese."""

           # 替换 sentiment_summariser
            self.sentiment_summariser = XFYunChat(
                appid=os.getenv("XFYUN_APPID"),
                api_key=os.getenv("XFYUN_API_KEY"),
                api_secret=os.getenv("XFYUN_API_SECRET"),
                system_prompt=sentiment_system_prompt
            )

            # evaluation_system_prompt = f"""
            # 你是一位专业的企业招聘顾问，负责撰写候选人的面试反馈。请以“**提供建设性反馈、鼓励成长**”为目标，为候选人输出一份**中文**的能力分析报告。
            #
            # 你将会收到以下信息：
            # 1. 岗位描述（Job Description）
            # 2. 面试转录文本（interview transcript）
            # 3. 情绪分析结果（如有）
            # 4. 候选人是否有事实性错误的分析（如有）
            # 5. 候选人的简历
            #
            # ⚠️ 如果部分信息缺失，请根据可用的内容（如面试文本和简历）进行评估。
            #
            # ---
            #
            # 请按以下格式输出反馈内容，全部使用中文，语气友好但客观：
            #
            # ---
            #
            # ### 🧠【能力评估】
            #
            # 请分别从以下五个维度，对候选人进行1~10分的打分，并结合面试中的具体回答，解释该得分的依据：
            #
            # 1. **沟通能力**（表达是否清晰、有条理）
            # 2. **专业能力**（岗位所需技能与经验）
            # 3. **问题解决能力**（是否能清晰分析、拆解问题）
            # 4. **工作态度与积极性**（表现出的热情、主动态度）
            # 5. **学习能力与成长潜力**（能否快速学习、适应变化）
            #
            # 每项请按照以下格式描述：
            # - 能力名称：X 分  （整数，范围为 1~10）
            # - 简要评语：一句总体总结
            # - 示例分析：引用面试中的具体回答（请用“例如他提到...”或“当被问及...”的方式）
            # - 如得分 ≤ 8 分，还请补充：
            #   - 改进建议（具体可行）
            #   - 推荐学习资料（如书籍、课程、方法）
            #
            # ---
            #
            # ### 📝【整体建议与下一步】
            #
            # 请根据候选人整体表现，判断是否通过面试。
            #
            # - 若推荐通过，请说明其优势，以及在哪些方面仍有进步空间
            # - 若暂不推荐，请表达委婉但清晰的拒绝，并鼓励其未来发展
            # - 最后用一句简短话结尾鼓励候选人继续努力
            #
            # ---
            #
            # ### ⚠️ 输出格式必须为中文，结构清晰。请避免使用英语。
            # """

            evaluation_system_prompt = """
            你是一位具备人力资源背景与面试行为分析经验的智能评估专家，目标是根据候选人的**面试表现**和**岗位匹配度**，生成一份结构化的评估反馈报告。

            你的任务是：
            - 动态评估候选人各项核心能力，给出量化评分（1~5分）
            - 提供**能力雷达图**可视化支持数据
            - 结合面试问答内容，定位关键问题，给出**结构化改进建议**
            - 根据整体表现，计算一个满分为100分的总评分，并做出最终推荐判断

            ---

            【评分标准说明】（所有单项能力评分统一使用 1～5 分）：
            - 5分：表现非常出色，远超岗位预期，有清晰证据支持
            - 4分：表现良好，达到岗位要求，偶有小缺陷
            - 3分：基本符合要求，存在可改善空间
            - 2分：略低于岗位要求，能力不足较明显
            - 1分：远未达标，表现存在较大短板

            【总评分说明】：
            请综合各项能力评分、岗位匹配度、情绪稳定性等维度，给出一个总评分（0~100分）：
            - ≥85：优秀，强烈推荐
            - 70~84：良好，可推荐
            - 60~69：一般，保留观察
            - ＜60：较弱，不建议录用

            ---

            【输入内容】（两个）：
            1. `chatlog`：面试过程结构化信息，包含：
               - 面试问题与候选人回答内容
               - 准确性分析（如：回答准确率、技术点覆盖、建议）
               - 情绪分析（如“紧张但表达清晰”）
            2. `job_resume_eval`：岗位匹配度与简历分析结果，包含：
               - 技能匹配度、经验匹配度、发展契合度评分与建议
               - 是否推荐、理由、简历优化建议

            ---

            【输出要求】：请使用如下 JSON 格式输出结构化反馈，字段说明如下：

            ```json
            {
              "ability_scores": {
                "专业知识水平": {"score": 4, "evidence": "在被问及Spring框架时回答准确，但未提及IOC机制" },
                "技能匹配度": {"score": 3, "evidence": "具备岗位核心技能，但缺少DevOps相关经验" },
                "语言表达能力": {"score": 4, "evidence": "回答流畅，逻辑清晰，有较强说服力" },
                "逻辑思维能力": {"score": 2, "evidence": "在拆解复杂问题时缺乏层次感，表达略显跳跃" },
                "应变与抗压能力": {"score": 3, "evidence": "面对追问时应对较好，情绪保持稳定" }
              },
              "radar_data": {
                "专业知识水平": 4,
                "技能匹配度": 3,
                "语言表达能力": 4,
                "逻辑思维能力": 2,
                "应变与抗压能力": 3
              },
              "problem_insights": [
                {
                  "dimension": "表达结构",
                  "issue": "部分回答缺乏条理，未使用结构化表达",
                  "suggestion": "建议使用 STAR 方法或总分总结构，提升表达清晰度"
                },
                {
                  "dimension": "逻辑思维能力",
                  "issue": "面对复杂问题拆解能力不足，缺乏系统性",
                  "suggestion": "练习问题分析与要点提炼，提升条理性"
                },
                {
                  "dimension": "应变与抗压能力",
                  "issue": "面对追问时略显紧张，回答流畅度受影响",
                  "suggestion": "增强心理素质训练，提高现场应变能力"
                },
                {
                  "dimension": "专业知识水平",
                  "issue": "部分技术细节回答不够准确或完整",
                  "suggestion": "加强相关技术理论学习，注重知识点补充"
                },
                {
                  "dimension": "技能匹配度",
                  "issue": "缺少部分岗位核心技能的实际经验",
                  "suggestion": "针对岗位技能需求，参与相关项目积累经验"
                }
              ],
              "overall_recommendation": {
                "decision": "建议通过 / 保留观察 / 暂不推荐",
                "reasoning": "候选人表现积极，专业能力基本达标，表达较好，但在问题拆解深度上有提升空间",
                "total_score": 78,
                "closing_remark": "请保持学习状态，相信你能在未来岗位中不断成长！"
              }
            }
            ```
            """

            cv_path = next((f for f in os.listdir(os.path.join(relate_path, "data/cvs")) if "active" in f), None)
            if cv_path is None:
                raise FileNotFoundError("No active CV file found in the 'data/cvs' directory.")
            cv_path = os.path.join(relate_path, "data/cvs", cv_path)
            # self.candidate_evaluator = ClaudeChatAssess("claude-3-5-sonnet-20240620", evaluation_system_prompt, cv_path)
            # 替换 candidate_evaluator
            self.candidate_evaluator = XFYunChat(
                appid=os.getenv("XFYUN_APPID"),
                api_key=os.getenv("XFYUN_API_KEY"),
                api_secret=os.getenv("XFYUN_API_SECRET"),
                system_prompt=evaluation_system_prompt,
                cv_path=cv_path  # 添加CV路径
            )
        except Exception as e:
            print(f"An error occurred during model setup: {e}")
            raise

    def reformat_chatlog(self):
        """
        Reformat the chatlog into a list of dictionaries.

        Returns:
            list: Reformatted chatlog.
        """
        dropped_context = self.chatlog[2:]
        outputchatlog = []

        for i in range(0, len(dropped_context), 2):
            if i + 1 < len(dropped_context):
                tempdict = {
                    'interviewer': dropped_context[i]['content'],
                    'candidate': dropped_context[i+1]['content']
                }
                outputchatlog.append(tempdict)
            else:
                break 

        return outputchatlog

    def rename_file_remove_active(self,filepath, filename):
        if "-active" not in filename:
            return filename  # 不包含active，不改名
        new_name = filename.replace("-active", "")
        old_path = os.path.join(filepath, filename)
        new_path = os.path.join(filepath, new_name)
        if os.path.exists(new_path):
            print(f"警告：目标文件 {new_path} 已存在，跳过重命名")
            return new_path
        if not os.path.exists(old_path):
            return filename
        os.rename(old_path, new_path)
        return new_name

    def process_sentiments(self,  sentiments=None):
        """
        Process sentiments for each audio file in the chatlog.

        Args:
            chatlog_chat (list): The reformatted chatlog.

        Returns:
            list: Chatlog with added sentiment analysis.
        """
        path = os.path.join(relate_path, 'data/interviews/')
        filepath = os.path.join(path, str(self.path_name), 'audio')
        print(f"Current working directory: {os.getcwd()}")
        print(f"Full audio directory path: {os.path.abspath(filepath)}")

        files = [f for f in os.listdir(filepath) if os.path.isfile(os.path.join(filepath, f))]
        
        # if len(chatlog_chat) < len(files):
        #     files = files[:len(chatlog_chat)]

        for f in files:
            print(f"File found: {f}")

        for count, file in enumerate(files, 1):
            if "-active" not in file:
                print(f"Skipping file {file} as it does not contain '-active'")
                continue
            full_file_path = os.path.join(filepath, file)
            print(f"Processing file: {full_file_path}")

            # 视频路径推测（可根据你的命名规则调整）
            video_path = os.path.join(os.path.dirname(filepath),'video',file.replace('.wav','.mp4'))
            audio_path = full_file_path
            output_file = os.path.join(os.path.dirname(filepath),'emotion_time_series',file.replace('.wav','.json'))
            self.output_files.append(output_file)
            text_path = os.path.join(os.path.dirname(filepath), 'text', file.replace('.wav', '.txt'))
            text = open(text_path, 'r',encoding='utf-8').read()
            print(f"Text: {text}")

            try:
                # 调用你自己的融合情绪分析函数
                result = generate_feedback(self.model,self.tokenizer,audio_path, video_path, text)
                sentiment_summary = self.sentiment_summariser.chat(str(result))
                print(f"Sentiment Summary: {sentiment_summary}")
                sentiments.append(sentiment_summary)

                # 重命名音频文件
                new_audio_file = self.rename_file_remove_active(filepath, file)
                # 重命名视频文件
                new_video_file = self.rename_file_remove_active(os.path.join(os.path.dirname(filepath), 'video'),
                                                           file.replace('.wav', '.mp4'))
                # 重命名文本文件
                new_text_file = self.rename_file_remove_active(os.path.join(os.path.dirname(filepath), 'text'),
                                                          file.replace('.wav', '.txt'))

                new_video_path = os.path.join(relate_path, 'data/interviews', self.path_name, "video" ,new_video_file)
                new_audio_path = os.path.join(relate_path, 'data/interviews', self.path_name, "audio" , new_audio_file)
                output_path = os.path.join(relate_path, 'data/interviews', self.path_name, 'emotion_time_series/emotion.json')

                if os.path.exists(new_video_path):
                    print("start_video_time", self.start_video_time)
                    _, self.start_video_time = extract_emotion_series(
                        detector=detector,
                        video_path=new_video_path,
                        audio_path=new_audio_path,
                        extractor=extractor,
                        model=audio_model,
                        classifier=classifier,
                        config=config,
                        interval_sec=2.0,
                        use_video= True,
                        output_json_path=output_path,
                        start_video_time=self.start_video_time,
                    )
                else:
                    _, self.start_video_time = extract_emotion_series(
                        detector=detector,
                        video_path=new_video_path,
                        audio_path=new_audio_path,
                        extractor=extractor,
                        model=audio_model,
                        classifier=classifier,
                        config=config,
                        interval_sec=2.0,
                        use_video=False,
                        output_json_path=output_path,
                        start_video_time=self.start_video_time,
                    )

                # sentiments.append((result, sentiment_summary))

                # 添加到 chatlog
                # chatlog_chat[count - 1]['sentiment'] = sentiment_summary

            except Exception as e:
                sentiment_summary = "Error processing file"
                sentiments.append(sentiment_summary)
                print(f"Error processing file {full_file_path}: {str(e)}")
                traceback.print_exc()

        # for count, file in enumerate(files, 1):
        #     full_file_path = os.path.join(filepath, file)
        #     print(f"Processing file: {full_file_path}")
        #
        #     # Add a small delay and re-check file existence
        #     time.sleep(0.1)
        #     if not os.path.exists(full_file_path):
        #         print(f"File not found (after delay): {full_file_path}")
        #         continue
        #
        #     try:
        #         result = self.sentiment_analyser.analyze_audio(full_file_path)
        #         sentiment_summary = self.sentiment_summariser.chat(str(result))
        #         sentiments.append((result, sentiment_summary))
        #         chatlog_chat[count-1]['sentiment'] = sentiment_summary
        #     except Exception as e:
        #         print(f"Error processing file {full_file_path}: {str(e)}")
        #         traceback.print_exc()
        #
        # self.chatlog_chat = chatlog_chat

    def save_sentiments(self, chatlog_chat, sentiments):
        print("sentiments:",len(sentiments))
        print("chatlog:",len(chatlog_chat))
        if len(chatlog_chat) != len(sentiments):
            print("Warning: Number of chat log entries and sentiments do not match.")
            return
        if not sentiments:
            print("No sentiments to save.")
            return
        for i in range(len(chatlog_chat)):
            chatlog_chat[i]['sentiment'] = sentiments[i]

    def save_feedbacks(self, chatlog_chat, feedbacks):
        print("chatlog:",len(chatlog_chat))
        print("feedbacks:",len(feedbacks))
        print(feedbacks)
        if len(chatlog_chat) != len(feedbacks):
            print("Warning: Number of chat log entries and feedbacks do not match.")
            return
        if not feedbacks:
            print("No feedbacks to save.")
            return
        for i in range(len(chatlog_chat)):
            chatlog_chat[i]['feedback'] = feedbacks[i]

    def evaluate_candidate(self, chatlog_chat,advice):
        """
        Evaluate the candidate based on the chatlog and sentiment analysis.

        Args:
            chatlog_chat (list): The chatlog with sentiment analysis.

        Returns:
            str: Evaluation result.
        """
        # 分析每个问答对
        # ConversationVerifier.process_qa_pair(chatlog_chat)
        # ConversationVerifier.process_qa_pair(chatlog_chat)   # chatlog_chat 是一个 list，它在函数里被就地修改了。
        # print("The Feedback JSON from the sentiment analyser and accuracy verifier: \n")
        # print(chatlog_chat)

        input_data = {
            "chatlog": json.dumps(chatlog_chat, ensure_ascii=False, indent=2),
            "job_resume_eval": json.dumps(advice, ensure_ascii=False, indent=2)
        }

        full_prompt = f"""
        请根据以下候选人面试表现和岗位匹配评估，生成结构化反馈：

        【面试记录】
        {chatlog_chat}

        【岗位匹配分析】
        {advice}
        """

        evaluation = self.candidate_evaluator.chat(full_prompt)
        # evaluation = self.candidate_evaluator.chat(str(chatlog_chat))
        chatlog_file_path = os.path.join(relate_path, f"data/interviews/{self.path_name}/outcome/")
        # Save outcome to file for convinience
        if not os.path.exists(chatlog_file_path):
            os.makedirs(chatlog_file_path)
        with open(chatlog_file_path+"chatlog.json", "w",encoding="utf-8") as file:
            json.dump(chatlog_chat, file, indent=4,ensure_ascii=False)
            # json.dump(chatlog_chat, file, indent=4)
        evaluation_file_path = os.path.join(relate_path, f"data/interviews/{self.path_name}/outcome/")
        if not os.path.exists(chatlog_file_path):
            os.makedirs(chatlog_file_path)
        with open(evaluation_file_path+"evaluation.json", "w",encoding="utf-8") as file:
            file.write(str(evaluation).replace('```json', '').replace('```', '').replace("\\n", "\n"))
            return str(evaluation).replace('```json', '').replace('```', '').replace("\\n", "\n")

    def run(self,feedbacks,advice):
        """
        Run the post-conversation processing pipeline.

        Returns:
            str: Final evaluation of the candidate.
        """
        # # 必须先处理情感分析，所有处理完成后再保存情感分析结果
        # sentiments = []
        # self.process_sentiments(sentiments)

        chatlog_chat = self.reformat_chatlog()
        self.save_feedbacks(chatlog_chat, feedbacks)
        # self.save_sentiments(chatlog_chat, sentiments)
        evaluation = self.evaluate_candidate(chatlog_chat,advice)
        print("------------------Evaluation----------------------")
        print(evaluation)
        return evaluation

    def handle_sentiments(self):
        self.process_sentiments(self.sentiments)

    def end_sentiments(self, feedbacks, advice, type):
        self.chatlog = load(os.path.join(self.directory, "joblib/conversation.joblib"))
        chatlog_chat = self.reformat_chatlog()
        self.save_feedbacks(chatlog_chat, feedbacks[1:])
        if type == "video":
            self.save_sentiments(chatlog_chat, self.sentiments[1:])
        evaluation = self.evaluate_candidate(chatlog_chat,advice)
        print("------------------Evaluation----------------------")
        print(evaluation)
        return evaluation

if __name__ == "__main__":
    model_path = os.path.join(relate_path, r'model/roberta-jd')
    tokenizer = BertTokenizer.from_pretrained(model_path)
    model = BertForSequenceClassification.from_pretrained(model_path)

    name = "杨璐雨"
    json_path = r"data/cvs/cv-deb-active.pdf"
    # cv_json = parse_resume(json_path)
    # print(cv_json)
    role = "前端开发工程师"
    job_description = """
        职位要求：
    1．熟悉 HTTP 协议、浏览器渲染原理
    2．熟悉HTML5/CSS3/JavaScript，了解ES6＋新特性
    3．熟悉 React / Vue 等常用前端框架，熟练使用 Tailwind CSS 和 TypeScript 
    4．熟悉 Vite 等构建工具，熟悉 NPM / Yarn 包管理
    5.熟练使用 Git 进行版本控制
    加分项：
    1.熟悉 Golang Gin Web 后端框架开发优先
    2.熟悉 Flutter 跨端开发工具者优先
        """
    # 简历匹配分析
    # optimizer = ResumeOptimizer(role, job_description)
    # advice = optimizer.optimize_resume(cv_json,name)
    with open(r'../../data/cvs/cv-niranj-feedback.json', 'r', encoding='utf-8') as f:
        advice = json.load(f)

    feedbacks = ['【准确率】：30%\n\n【反馈】：候选人仅提到去噪处理，但未具体说明采用的方法（如高斯滤波、中值滤波等），也未涉及如何处理不完整目标的关键步骤（如形态学操作或目标重建算法）。回答过于简略且缺乏技术细节支撑。\n\n【改进建议】：\n– 明确说明具体的去噪方法（例如：使用高斯滤波去除高斯噪声，或用中值滤波抑制椒盐噪声）\n– 补充针对不完整目标的处理方法（例如：通过形态学闭运算填充目标空洞，或基于轮廓匹配重建目标边界）\n– 可简要提及参数选择依据（如滤波核大小与目标尺寸的关系）',
                 '【准确率】：40%\n\n【反馈】：候选人仅列举了两种基础去噪方法（平滑滤波、高斯滤波），但未说明具体实现原理和适用场景。回答缺乏对其他重要去噪方法的覆盖，且未体现分类讨论噪声类型（如椒盐噪声、高斯噪声）的针对性处理思路。\n\n【改进建议】：\n– 补充不同噪声类型的对应处理方法（如中值滤波针对椒盐噪声）\n– 增加频域去噪方法（如傅里叶变换后滤波）\n– 说明自适应滤波（如非局部均值去噪）或深度学习方法（如DnCNN）\n– 简要比较各方法优缺点及适用条件']


    processor = PostConversationProcessor("Dawn/202507042024",0.47,model,tokenizer)
    # processor.end_sentiments(feedbacks,advice)
