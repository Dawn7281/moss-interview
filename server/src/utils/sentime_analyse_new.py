import json
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"  # ✅ 禁用 oneDNN
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"   # ✅ 静音日志（可选）
import time
from collections import defaultdict
import numpy as np
import ffmpeg
import cv2
import librosa
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from fer import FER
from transformers import AutoFeatureExtractor, HubertModel, AutoConfig
import torch.nn.functional as F

relate_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def extract_audio_features(audio_path):
    y, sr = librosa.load(audio_path)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    energy = librosa.feature.rms(y=y)
    duration = librosa.get_duration(y=y, sr=sr)
    return {
        "mfcc_mean": mfcc.mean(axis=1).tolist(),
        "mfcc_std": mfcc.std(axis=1).tolist(),
        "energy_mean": energy.mean().item(),
        "duration": duration,
        "sample_rate": sr
    }

def load_local_model(save_dir: str):
    print(f"从本地目录加载模型：{save_dir}")
    extractor = AutoFeatureExtractor.from_pretrained(save_dir)
    model = HubertModel.from_pretrained(save_dir)
    config = AutoConfig.from_pretrained(save_dir)

    classifier = torch.nn.Sequential(
        torch.nn.Linear(config.hidden_size, config.hidden_size),
        torch.nn.Tanh(),
        torch.nn.Dropout(config.classifier_dropout),
        torch.nn.Linear(config.hidden_size, 6)
    )
    classifier.eval()
    model.eval()
    return extractor, model, classifier, config

def predict_emotion(audio_path: str, extractor, model, classifier, config, sample_rate=16000, max_duration=6):
    y, _ = librosa.load(audio_path, sr=sample_rate)
    if len(y) > sample_rate * max_duration:
        y = y[:sample_rate * max_duration]
    else:
        y = librosa.util.fix_length(y, size=sample_rate * max_duration)

    inputs = extractor(y, sampling_rate=sample_rate, return_tensors="pt", padding=True).input_values
    with torch.no_grad():
        features = model(inputs).last_hidden_state
        pooled = features.mean(dim=1)
        logits = classifier(pooled)
        probs = F.softmax(logits, dim=-1)[0].cpu().numpy()

    labels = ['angry','fear','happy','neutral','sad','surprise','disgust']
    idx = probs.argmax()
    return labels[idx], float(probs[idx]), dict(zip(labels, map(float, probs)))

def map_to_interview_emotions(emotions):
    """
    将原始7类FER情绪映射为更高层次的面试情绪标签。
    输入: emotions - dict, FER情绪输出
    输出: dict, 5种面试情绪
    """
    return {
        "confidence": emotions["happy"] * 0.7 + emotions["neutral"] * 0.3,
        "nervousness": emotions["fear"] * 0.6 + emotions["sad"] * 0.3 + emotions["neutral"] * -0.2,
        "frustration": emotions["sad"] * 0.6 + emotions["disgust"] * 0.4,
        "attentiveness": emotions["neutral"],
        "confusion": emotions["surprise"] * 0.8 + emotions["fear"] * 0.2
    }

# def extract_video_emotion_time_series(video_path, output_file, a=1.0, b=10, min_frames=30, max_frames=120):
#     cap = cv2.VideoCapture(video_path)
#     if not cap.isOpened():
#         print("视频打开失败，请检查路径或文件格式")
#         return
#
#     detector = FER(mtcnn=True)
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     duration_sec = total_frames / fps
#
#     target_frames = int(a * duration_sec + b)
#     target_frames = max(min(target_frames, max_frames), min_frames)
#     interval = max(1, total_frames // target_frames)
#
#     emotion_time_series = []
#     interview_emotion_series = []
#     detected_faces = 0
#     extracted = 0
#     frame_idx = 0
#
#     while extracted < target_frames and frame_idx < total_frames:
#         cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
#         ret, frame = cap.read()
#         if not ret:
#             print(f"Frame {frame_idx} 读取失败")
#             break
#
#         results = detector.detect_emotions(frame)
#         if results:
#             detected_faces += len(results)
#             emotions = results[0]["emotions"]
#             interview_emotions = map_to_interview_emotions(emotions)
#
#             emotion_time_series.append({
#                 "frame": frame_idx,
#                 "time_sec": frame_idx / fps,
#                 "emotions": emotions,
#                 "interview_emotions": interview_emotions
#             })
#             interview_emotion_series.append(interview_emotions)
#
#         extracted += 1
#         frame_idx += interval
#
#     cap.release()
#
#     if emotion_time_series:
#         emotion_keys = emotion_time_series[0]['emotions'].keys()
#         avg_emotions = {
#             k: float(np.mean([item['emotions'][k] for item in emotion_time_series]))
#             for k in emotion_keys
#         }
#         interview_keys = emotion_time_series[0]['interview_emotions'].keys()
#         avg_interview_emotions = {
#             k: float(np.mean([item['interview_emotions'][k] for item in emotion_time_series]))
#             for k in interview_keys
#         }
#     else:
#         avg_emotions = {}
#         avg_interview_emotions = {}
#
#     # 保存 emotion_time_series 到文件
#     if not os.path.exists(os.path.dirname(output_file)):
#         os.makedirs(os.path.dirname(output_file))
#     with open(output_file, "w", encoding="utf-8") as ef:
#         json.dump(emotion_time_series, ef, ensure_ascii=False, indent=2)
#
#     return {
#         "frame_count": total_frames,
#         "video_duration_sec": duration_sec,
#         "target_frames": target_frames,
#         "detected_faces": detected_faces,
#         "avg_emotions": avg_emotions,
#         "avg_interview_emotions": avg_interview_emotions
#     }

def extract_video_avg_emotion(video_path, num_frames=50):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("视频打开失败，请检查路径")
        return None

    detector = FER(mtcnn=True)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    interval = max(1, total_frames // num_frames)
    emotion_accumulator = []
    detected_faces = 0

    for i in range(0, total_frames, interval):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if not ret:
            continue

        results = detector.detect_emotions(frame)
        if results:
            emotions = results[0]["emotions"]
            emotion_accumulator.append(emotions)
            detected_faces += 1

        if len(emotion_accumulator) >= num_frames:
            break

    cap.release()

    if not emotion_accumulator:
        return {"avg_emotions": {}, "detected_faces": 0}

    # 平均每个情绪维度
    emotion_keys = emotion_accumulator[0].keys()
    avg_emotions = {
        k: float(np.mean([e[k] for e in emotion_accumulator]))
        for k in emotion_keys
    }

    return {
        "avg_emotions": avg_emotions,
        "detected_faces": detected_faces,
        "video_duration_sec": total_frames / fps,
        "frames_used": len(emotion_accumulator)
    }



def extract_text_predictions(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=1)[0].cpu().numpy()
        pred = int(np.argmax(probs))

    sentiment = [
        {"name": "positive", "score": float(probs[1])},
        {"name": "negative", "score": float(probs[0])}
    ]

    # 假设我们无法准确分析“toxicity”和“emotions”，可以设为空
    result = {
        "emotions": [],
        "sentiment": sentiment,
        "toxicity": []
    }

    return [{
        "results": {
            "predictions": [{
                "models": {
                    "language": {
                        "grouped_predictions": [{
                            "predictions": [result]
                        }]
                    }
                }
            }]
        }
    }]


def extract_audio_predictions(audio_path,audio_model):
    features = extract_audio_features(audio_path)
    energy = features["energy_mean"]
    mfcc_mean = np.mean(np.abs(features["mfcc_mean"]))

    emotion, confidence, probs = predict_emotion(audio_path, extractor, audio_model, classifier, config)
    emotions = [{"name": k, "score": round(v, 3)} for k, v in probs.items()]

    # 简单映射，示意
    toxicity = [
        {"name": "toxicity", "score": round((mfcc_mean / 100.0 + energy / 1.0) / 2.0, 3)}
    ]

    result = {
        "emotions": emotions,
        "sentiment": [],  # 音频无直接情感极性标签
        "toxicity": toxicity
    }

    return [{
        "results": {
            "predictions": [{
                "models": {
                    "audio": {
                        "grouped_predictions": [{
                            "predictions": [result]
                        }]
                    }
                }
            }]
        }
    }]


def extract_video_predictions(video_path):
    # data = extract_video_emotion_time_series(video_path, output_file)
    data = extract_video_avg_emotion(video_path, num_frames=50)
    interview_emotions = data.get("avg_interview_emotions", {})

    emotions = [{"name": k, "score": round(v, 3)} for k, v in interview_emotions.items()]

    result = {
        "emotions": emotions,
        "sentiment": [],  # 视频不提供正负向判断
        "toxicity": []  # 视频不分析毒性
    }

    return [{
        "results": {
            "predictions": [{
                "models": {
                    "vision": {
                        "grouped_predictions": [{
                            "predictions": [result]
                        }]
                    }
                }
            }]
        }
    }]

def _extract_modal_scores(modal_predictions, modal_type):
    """
    从一个模态中提取 emotions / sentiment / toxicity。

    Args:
        modal_predictions (list): Hume格式的预测结果。
        modal_type (str): 'text'、'audio' 或 'video'。

    Returns:
        dict: 包含 emotions / sentiments / toxicity 的提取结果。
    """
    # 映射 modal_type 到 Hume 模型键
    model_key_map = {
        "text": "language",
        "audio": "audio",
        "video": "vision"
    }

    model_key = model_key_map.get(modal_type)
    if model_key is None:
        raise ValueError(f"未知的 modal_type: {modal_type}")

    try:
        pred = modal_predictions[0]['results']['predictions'][0]['models'][model_key]['grouped_predictions'][0]['predictions'][0]
    except (KeyError, IndexError) as e:
        print(f"[错误] 模态 '{modal_type}' 提取失败: {e}")
        return {}

    result = {}

    # 按模态不同选择输出结构
    result['emotions'] = {e['name']: e['score'] for e in pred.get('emotions', [])}
    if modal_type == 'text':
        result['sentiments'] = {s['name']: s['score'] for s in pred.get('sentiment', [])}
        result['toxicity'] = {t['name']: t['score'] for t in pred.get('toxicity', [])}
    elif modal_type == 'audio':
        result['toxicity'] = {t['name']: t['score'] for t in pred.get('toxicity', [])}
    # video 不含 sentiments/toxicity

    return result


def _fuse_modal_scores(modal_results, weights):
    """
    modal_results: list of dicts like [{'emotions': {...}}, {...}, ...]
    weights: dict like {'text': 0.4, 'audio': 0.3, 'video': 0.3}
    """
    fused = {
        "emotions": defaultdict(float),
        "sentiments": defaultdict(float),
        "toxicity": defaultdict(float),
    }
    for modal_type, result in modal_results.items():
        weight = weights.get(modal_type, 0)
        for key in ['emotions', 'sentiments', 'toxicity']:
            for label, score in result.get(key, {}).items():
                fused[key][label] += score * weight

    # 转 float & round
    return {
        key: {label: round(score, 3) for label, score in score_dict.items()}
        for key, score_dict in fused.items()
    }

def _process_predictions(text_preds=None, audio_preds=None, video_preds=None, weights=None):
    if weights is None:
        weights = {'text': 0.4, 'audio': 0.3, 'video': 0.3}

    results = {}
    if text_preds:
        results['text'] = _extract_modal_scores(text_preds, 'text')
    if audio_preds:
        results['audio'] = _extract_modal_scores(audio_preds, 'audio')
    if video_preds:
        results['video'] = _extract_modal_scores(video_preds, 'video')

    fused_result = _fuse_modal_scores(results, weights)

    return fused_result


def generate_feedback(model, tokenizer, audio_path, video_path, text):
    # 初始化各模态预测为 None
    text_predictions = None
    audio_predictions = None
    video_predictions = None

    # 提取文本情绪
    if text and model and tokenizer:
        text_predictions = extract_text_predictions(text, tokenizer, model)

    # 提取音频特征
    if os.path.exists(audio_path):
        audio_predictions = extract_audio_predictions(audio_path,audio_model)

    # 提取视频情绪
    if os.path.exists(video_path):
        video_predictions = extract_video_predictions(video_path)

    # 动态计算权重（只对存在的模态赋权）
    all_preds = {
        'text': text_predictions,
        'audio': audio_predictions,
        'video': video_predictions
    }
    available_modalities = {k: v for k, v in all_preds.items() if v is not None}
    if not available_modalities:
        return {"error": "没有可用的模态输入，至少需要一个 text/audio/video"}

    # 平均分配权重
    modal_count = len(available_modalities)
    weights = {k: round(1.0 / modal_count, 3) for k in available_modalities}

    # 处理所有模态预测
    final_result = _process_predictions(
        text_preds=text_predictions,
        audio_preds=audio_predictions,
        video_preds=video_predictions,
        weights=weights
    )

    return final_result

save_dir = os.path.join(relate_path, r"model/chinese_emotion_model")  # 本地模型目录
extractor, audio_model, classifier, config = load_local_model(save_dir)


def predict_emotion_from_array(audio_array, extractor, model, classifier, sample_rate=16000):
    # 提取特征
    inputs = extractor(audio_array, sampling_rate=sample_rate, return_tensors="pt", padding=True).input_values

    # 模型推理
    with torch.no_grad():
        features = model(inputs).last_hidden_state
        pooled = features.mean(dim=1)
        logits = classifier(pooled)
        probs = F.softmax(logits, dim=-1)[0].cpu().numpy()

    # 情绪标签
    labels = ['angry', 'fear', 'happy', 'neutral', 'sad', 'surprise']
    audio_emotion = dict(zip(labels, map(float, probs)))
    audio_emotion['disgust'] = 0.0  # 补上缺失项
    idx = probs.argmax()
    return labels[idx], float(probs[idx]), audio_emotion

# 多模态融合主函数
# def extract_multimodal_emotion_series(detector,video_path, audio_path, extractor, model, classifier, config,
#                                       interval_sec=2.0, output_json_path=None):
#     cap = cv2.VideoCapture(video_path)
#     if not cap.isOpened():
#         print("视频读取失败")
#         return []
#
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     video_duration = total_frames / fps
#
#     y, sr = librosa.load(audio_path, sr=16000)
#     total_segments = int(video_duration // interval_sec)
#
#     emotion_series = []
#
#     for i in range(total_segments):
#         start_time = i * interval_sec
#         end_time = (i + 1) * interval_sec
#
#         # 1. 提取视频帧（取段中间一帧）
#         target_frame = int(((start_time + end_time) / 2) * fps)
#         cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
#         ret, frame = cap.read()
#         video_emotion = {}
#         if ret:
#             results = detector.detect_emotions(frame)
#             if results:
#                 raw_emotions = results[0]["emotions"]
#                 video_emotion = raw_emotions
#             else:
#                 video_emotion = {k: 0.0 for k in ['angry', 'fear', 'happy', 'neutral', 'sad', 'surprise', 'disgust']}
#         else:
#             video_emotion = {k: 0.0 for k in ['angry', 'fear', 'happy', 'neutral', 'sad', 'surprise', 'disgust']}
#
#         # 2. 音频切片 + 情绪识别
#         audio_start = int(sr * start_time)
#         audio_end = int(sr * end_time)
#         # audio_slice = y[audio_start:audio_end]
#         # if len(audio_slice) < sr * interval_sec:
#         #     audio_slice = librosa.util.fix_length(audio_slice, size=int(sr * interval_sec))
#
#         target_len = int(sr * (end_time - start_time))
#
#         if audio_start >= len(y):
#             # 超出音频范围，返回静音段v
#             return np.zeros(target_len, dtype=np.float32)
#
#         if audio_end > len(y):
#             audio_end = len(y)
#
#         audio_slice = y[audio_start:audio_end]
#
#         # 补零或截断
#         target_len = int(sr * (end_time - start_time))
#         if len(audio_slice) < target_len:
#             audio_slice = librosa.util.fix_length(audio_slice, size=target_len)
#         else:
#             audio_slice = audio_slice[:target_len]
#
#         label, prob, audio_emotion = predict_emotion_from_array(
#             audio_slice, extractor, model, classifier, sample_rate=sr
#         )
#
#         # 3. 情绪融合
#         fused_emotion = {
#             k: round(0.5 * video_emotion.get(k, 0) + 0.5 * audio_emotion.get(k, 0), 4)
#             for k in ['angry', 'fear', 'happy', 'neutral', 'sad', 'surprise','disgust']
#         }
#
#         # 4. 映射到面试情绪
#         interview_emotions = map_to_interview_emotions(fused_emotion)
#
#
#         # 4. 添加到序列
#         emotion_series.append({
#             "time_sec": round(start_time, 2),
#             # "video_emotion": video_emotion,
#             # "audio_emotion": audio_emotion,
#             # "fused_emotion": fused_emotion,
#             "interview_emotions": interview_emotions,
#         })
#
#     cap.release()
#
#     # 5. 保存到 JSON 文件
#     os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
#     with open(output_json_path, "w", encoding="utf-8") as f:
#         json.dump(emotion_series, f, ensure_ascii=False, indent=2)
#
#     print(f"情绪时间序列已保存到 {output_json_path}")
#
#     return emotion_series

def extract_emotion_series(detector=None,
                           video_path=None,
                           audio_path=None,
                           extractor=None,
                           model=None,
                           classifier=None,
                           config=None,
                           interval_sec=2.0,
                           output_json_path=None,
                           use_video=True):
    """
    通用情绪提取函数，支持音频和多模态（音频 + 视频）。

    :param detector: 面部情绪检测器（可为None，若 use_video=False 则忽略）
    :param video_path: 视频文件路径
    :param audio_path: 音频文件路径
    :param extractor: 音频特征提取器
    :param model: 音频模型
    :param classifier: 音频分类器
    :param config: 其他配置参数（可选）
    :param interval_sec: 情绪采样间隔（秒）
    :param output_json_path: 结果保存路径（.json）
    :param use_video: 是否使用视频（False 表示只用音频）
    :return: 情绪时间序列（list）
    """
    emotion_series = []

    # === 加载音频 ===
    y, sr = librosa.load(audio_path, sr=16000)
    audio_duration = len(y) / sr
    total_segments = int(audio_duration // interval_sec)

    if use_video:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("视频读取失败，转为仅音频模式")
            use_video = False
        else:
            fps = cap.get(cv2.CAP_PROP_FPS)

    for i in range(total_segments):
        start_time = i * interval_sec
        end_time = (i + 1) * interval_sec

        # === 视频帧处理 ===
        video_emotion = {k: 0.0 for k in ['angry', 'fear', 'happy', 'neutral', 'sad', 'surprise', 'disgust']}
        if use_video:
            target_frame = int(((start_time + end_time) / 2) * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
            ret, frame = cap.read()
            if ret:
                results = detector.detect_emotions(frame)
                if results:
                    video_emotion = results[0]["emotions"]

        # === 音频切片 ===
        audio_start = int(sr * start_time)
        audio_end = int(sr * end_time)

        if audio_start >= len(y):
            break
        if audio_end > len(y):
            audio_end = len(y)

        audio_slice = y[audio_start:audio_end]
        target_len = int(sr * interval_sec)
        audio_slice = librosa.util.fix_length(audio_slice, size=target_len)

        label, prob, audio_emotion = predict_emotion_from_array(
            audio_slice, extractor, model, classifier, sample_rate=sr
        )

        # === 情绪融合（或直接使用音频）===
        if use_video:
            fused_emotion = {
                k: round(0.5 * video_emotion.get(k, 0) + 0.5 * audio_emotion.get(k, 0), 4)
                for k in ['angry', 'fear', 'happy', 'neutral', 'sad', 'surprise', 'disgust']
            }
        else:
            fused_emotion = audio_emotion

        interview_emotions = map_to_interview_emotions(fused_emotion)

        emotion_series.append({
            "time_sec": round(start_time, 2),
            "interview_emotions": interview_emotions,
        })

    if use_video:
        cap.release()

    # === 保存结果 ===
    if output_json_path:
        os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(emotion_series, f, ensure_ascii=False, indent=2)
        print(f"情绪时间序列已保存到 {output_json_path}")
    # 5. 保存到 JSON 文件
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    # 读取现有数据
    existing_data = []
    if os.path.exists(output_json_path):
        try:
            with open(output_json_path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
                if not isinstance(existing_data, list):
                    existing_data = []
        except (json.JSONDecodeError, FileNotFoundError):
            existing_data = []

    # 追加新数据
    existing_data.extend(emotion_series)

    # 保存
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)
    # with open(output_json_path, "w", encoding="utf-8") as f:
    #     json.dump(emotion_series, f, ensure_ascii=False, indent=2)

    print(f"情绪时间序列已保存到 {output_json_path}")

    return emotion_series


def extract_emotion_series(detector=None,
                           video_path=None,
                           audio_path=None,
                           extractor=None,
                           model=None,
                           classifier=None,
                           config=None,
                           interval_sec=2.0,
                           output_json_path=None,
                           use_video=True,
                           start_video_time=0.0):
    """
    通用情绪提取函数，支持音频和多模态（音频 + 视频）。

    :param detector: 面部情绪检测器（可为None，若 use_video=False 则忽略）
    :param video_path: 视频文件路径
    :param audio_path: 音频文件路径
    :param extractor: 音频特征提取器
    :param model: 音频模型
    :param classifier: 音频分类器
    :param config: 其他配置参数（可选）
    :param interval_sec: 情绪采样间隔（秒）
    :param output_json_path: 结果保存路径（.json）
    :param use_video: 是否使用视频（False 表示只用音频）
    :return: 情绪时间序列（list）
    """
    emotion_series = []

    # === 加载音频 ===
    y, sr = librosa.load(audio_path, sr=16000)
    audio_duration = len(y) / sr
    total_segments = int(audio_duration // interval_sec)

    if use_video:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("视频读取失败，转为仅音频模式")
            use_video = False
        else:
            fps = cap.get(cv2.CAP_PROP_FPS)

    for i in range(total_segments):
        start_time = i * interval_sec
        end_time = (i + 1) * interval_sec

        # === 视频帧处理 ===
        video_emotion = {k: 0.0 for k in ['angry', 'fear', 'happy', 'neutral', 'sad', 'surprise', 'disgust']}
        if use_video:
            target_frame = int(((start_time + end_time) / 2) * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
            ret, frame = cap.read()
            if ret:
                results = detector.detect_emotions(frame)
                if results:
                    video_emotion = results[0]["emotions"]

        # === 音频切片 ===
        audio_start = int(sr * start_time)
        audio_end = int(sr * end_time)

        if audio_start >= len(y):
            break
        if audio_end > len(y):
            audio_end = len(y)

        audio_slice = y[audio_start:audio_end]
        target_len = int(sr * interval_sec)
        audio_slice = librosa.util.fix_length(audio_slice, size=target_len)

        label, prob, audio_emotion = predict_emotion_from_array(
            audio_slice, extractor, model, classifier, sample_rate=sr
        )

        # === 情绪融合（或直接使用音频）===
        if use_video:
            fused_emotion = {
                k: round(0.5 * video_emotion.get(k, 0) + 0.5 * audio_emotion.get(k, 0), 4)
                for k in ['angry', 'fear', 'happy', 'neutral', 'sad', 'surprise', 'disgust']
            }
        else:
            fused_emotion = audio_emotion

        interview_emotions = map_to_interview_emotions(fused_emotion)

        emotion_series.append({
            "time_sec": round(start_time + start_video_time, 2),
            "interview_emotions": interview_emotions,
        })

    start_video_time += audio_duration

    if use_video:
        cap.release()

    # === 保存结果 ===
    if output_json_path:
        os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(emotion_series, f, ensure_ascii=False, indent=2)
        print(f"情绪时间序列已保存到 {output_json_path}")

    return emotion_series, start_video_time

if __name__ == "__main__":
    # audio_path = r"..\..\data\interviews\Dawn1747984120-2\audio\recording-2025-05-23T070928.wav"
    # video_path = r"..\..\data\interviews\Dawn1747984120-2\speech\recording_20250523_150947.mp3"
    # text = " My name is转走。Thank you for your time talking the time to speak with me today about the entry level，machine learning，engineer position。"
    # output_file = r"..\..\data\interviews\Dawn1747984120-2\emotion_time_series\前端面试情绪.json"
    # feedback = generate_feedback(audio_path, video_path, text, output_file)
    # print("生成的反馈：", feedback)

    # 模型加载（建议移动到函数外部避免重复加载）
    model_path = r'../../model/roberta-jd'
    tokenizer = BertTokenizer.from_pretrained(model_path)
    model = BertForSequenceClassification.from_pretrained(model_path)

    # 音频模型加载
    save_dir = r"..\..\model\chinese_emotion_model"  # 本地模型目录
    extractor, audio_model, classifier, config = load_local_model(save_dir)

    # 初始化 FER 检测器
    detector = FER(mtcnn=True)

    audio_path = r"..\..\data\test\audio\前端面试.wav"
    # audio_path = None
    # video_path = r"..\..\data\test\video\前端面试.mp4"
    video_path = None
    text = "你好，很高兴参加面试"
    output_path = r"..\..\data\test\mul\a.json"
    # final_result = generate_feedback(model,tokenizer,audio_path,video_path,text)
    # print("最终结果：", final_result)

    result = extract_emotion_series(
        detector=detector,
        video_path=video_path,
        audio_path=audio_path,
        extractor=extractor,
        model=audio_model,
        classifier=classifier,
        config=config,
        interval_sec=2.0,
        use_video=False,
        output_json_path=output_path
    )