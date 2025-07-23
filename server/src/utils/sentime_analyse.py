import json
import os
import time
import numpy as np
import ffmpeg
import cv2
from fer import FER
import librosa
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from fer import FER

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

def extract_video_emotion_time_series(video_path, output_file, a=1.0, b=10, min_frames=30, max_frames=120):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("视频打开失败，请检查路径或文件格式")
        return

    detector = FER(mtcnn=True)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration_sec = total_frames / fps

    target_frames = int(a * duration_sec + b)
    target_frames = max(min(target_frames, max_frames), min_frames)
    interval = max(1, total_frames // target_frames)

    emotion_time_series = []
    interview_emotion_series = []
    detected_faces = 0
    extracted = 0
    frame_idx = 0

    while extracted < target_frames and frame_idx < total_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            print(f"Frame {frame_idx} 读取失败")
            break

        results = detector.detect_emotions(frame)
        if results:
            detected_faces += len(results)
            emotions = results[0]["emotions"]
            interview_emotions = map_to_interview_emotions(emotions)

            emotion_time_series.append({
                "frame": frame_idx,
                "time_sec": frame_idx / fps,
                "emotions": emotions,
                "interview_emotions": interview_emotions
            })
            interview_emotion_series.append(interview_emotions)

        extracted += 1
        frame_idx += interval

    cap.release()

    if emotion_time_series:
        emotion_keys = emotion_time_series[0]['emotions'].keys()
        avg_emotions = {
            k: float(np.mean([item['emotions'][k] for item in emotion_time_series]))
            for k in emotion_keys
        }
        interview_keys = emotion_time_series[0]['interview_emotions'].keys()
        avg_interview_emotions = {
            k: float(np.mean([item['interview_emotions'][k] for item in emotion_time_series]))
            for k in interview_keys
        }
    else:
        avg_emotions = {}
        avg_interview_emotions = {}

    # 保存 emotion_time_series 到文件
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))
    with open(output_file, "w", encoding="utf-8") as ef:
        json.dump(emotion_time_series, ef, ensure_ascii=False, indent=2)

    return {
        "frame_count": total_frames,
        "video_duration_sec": duration_sec,
        "target_frames": target_frames,
        "detected_faces": detected_faces,
        "avg_emotions": avg_emotions,
        "avg_interview_emotions": avg_interview_emotions
    }


# def extract_video_emotion_time_series(video_path,output_file, a=1.0, b=10, min_frames=30, max_frames=120):
#     cap = cv2.VideoCapture(video_path)
#     if not cap.isOpened():
#         print("视频打开失败，请检查路径或文件格式")
#         return
#     detector = FER(mtcnn=True)
#
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     print(f"总帧数: {total_frames}, FPS: {fps}")
#     duration_sec = total_frames / fps
#
#     # 动态确定目标帧数，限制最大帧数
#     target_frames = int(a * duration_sec + b)
#     target_frames = max(min(target_frames, max_frames), min_frames)
#
#     # 均匀抽帧
#     interval = max(1, total_frames // target_frames)
#
#     emotion_time_series = []
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
#         # print(f"Frame {frame_idx} 检测结果: {results}")  # 看是否检测到人脸和情绪
#         if results:
#             detected_faces += len(results)
#             emotions = results[0]["emotions"]
#             emotion_time_series.append({
#                 "frame": frame_idx,
#                 "time_sec": frame_idx / fps,
#                 "emotions": emotions
#             })
#
#         extracted += 1
#         frame_idx += interval
#
#     cap.release()
#
#     # 计算平均情绪
#     if emotion_time_series:
#         emotion_keys = emotion_time_series[0]['emotions'].keys()
#         avg_emotions = {
#             k: float(np.mean([item['emotions'][k] for item in emotion_time_series]))
#             for k in emotion_keys
#         }
#     else:
#         avg_emotions = {}
#
#     # 保存 emotion_time_series 到独立文件
#     emotion_path = output_file
#     if not os.path.exists(os.path.dirname(emotion_path)):
#         os.makedirs(os.path.dirname(emotion_path))
#     with open(emotion_path, "w", encoding="utf-8") as ef:
#         json.dump(emotion_time_series, ef, ensure_ascii=False, indent=2)
#
#     return {
#         "frame_count": total_frames,
#         "video_duration_sec": duration_sec,
#         "target_frames": target_frames,
#         "detected_faces": detected_faces,
#         "avg_emotions": avg_emotions
#     }


def analyze_text_sentiment(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=1)[0].cpu().numpy()
        pred = int(np.argmax(probs))
    label_map = {0: "负向", 1: "正向"}
    return {
        "文本内容": text,
        "情绪概率": probs.tolist(),
        "预测标签": label_map[pred],
        "预测置信度": float(probs[pred])
    }

def main():
    AUDIO_PATH = r"D:\AllFiles\competition\soft\Screening-LLM\data\test\前端面试.wav"
    VIDEO_PATH = r"D:\AllFiles\competition\soft\Screening-LLM\data\test\前端面试.mp4"
    output_dir = r"D:\AllFiles\competition\soft\Screening-LLM\data\test"

    # 提取音频
    print("开始提取音频……")
    # extract_audio_from_video(VIDEO_PATH, AUDIO_PATH)

    print("开始提取音频特征……")
    audio_feat = extract_audio_features(AUDIO_PATH)

    print("开始提取视频情绪时间序列……")
    video_emotion_data = extract_video_emotion_time_series(VIDEO_PATH,output_dir)

    print("开始分析文本情绪……")
    model_path = r'D:\AllFiles\competition\soft\Screening-LLM\model\roberta-jd'
    tokenizer = BertTokenizer.from_pretrained(model_path)
    model = BertForSequenceClassification.from_pretrained(model_path)
    text = "你好，我很高兴参加面试"
    text_sentiment = analyze_text_sentiment(text, tokenizer, model)

    fused_result = {
        "音频特征": audio_feat,
        "视频情绪": video_emotion_data,
        "文本情绪": text_sentiment
    }

    output_json = os.path.join(output_dir, "multi_modal_result.json")
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(fused_result, f, ensure_ascii=False, indent=4)

    print(f"分析结果已保存到 {output_json}")

def generate_feedback(audio_path, video_path, text, output_file):
    # 提取音频特征
    audio_feat = extract_audio_features(audio_path)

    # 提取视频情绪
    video_emotion_data = extract_video_emotion_time_series(video_path, output_file)
    avg_emotions = video_emotion_data.get('avg_emotions', {})  # 应是类似 {'angry': 0.1, ...}

    # 文本情绪分析
    model_path = os.path.join(relate_path, r'model/roberta-jd')
    tokenizer = BertTokenizer.from_pretrained(model_path)
    model = BertForSequenceClassification.from_pretrained(model_path)
    text_sentiment = analyze_text_sentiment(text, tokenizer, model)

    # === 计算结构化输出 ===

    # === 音频毒性打分逻辑 ===
    audio_energy = audio_feat.get("energy_mean", 0.0)
    mfcc_values = audio_feat.get("mfcc_mean", [])
    mfcc_avg = float(np.mean(np.abs(mfcc_values))) if isinstance(mfcc_values, list) and mfcc_values else 0.0

    # print("DEBUG - audio_energy:", audio_energy)
    # print("DEBUG - mfcc_avg:", mfcc_avg)
    # print("DEBUG - text_sentiment:", text_sentiment)

    # 归一化处理，避免mfcc主导
    audio_toxicity_score = float(np.clip((audio_energy / 1.0 + mfcc_avg / 100.0) / 2.0, 0, 1))

    # === 文本情绪得分 ===
    label = text_sentiment.get("预测标签", "")
    confidence = float(text_sentiment.get("预测置信度", 0.0))
    sentiment_score = confidence
    if label == "负向":
        sentiment_score = 1 - confidence

    # === 构造最终反馈结构 ===
    fused_result = {
        "emotions": avg_emotions,
        "sentiments": {
            "text_sentiment": round(sentiment_score, 3)
        },
        "toxicity": {
            "audio_toxicity": round(audio_toxicity_score, 3)
        }
    }

    return fused_result

if __name__ == "__main__":
    # audio_path = r"D:\AllFiles\competition\soft\Screening-LLM\data\interviews\Dawn1747984120-2\audio\recording-2025-05-23T070928.wav"
    # video_path = r"D:\AllFiles\competition\soft\Screening-LLM\data\interviews\Dawn1747984120-2\speech\recording_20250523_150947.mp3"
    # text = " My name is转走。Thank you for your time talking the time to speak with me today about the entry level，machine learning，engineer position。"
    # output_file = r"D:\AllFiles\competition\soft\Screening-LLM\data\interviews\Dawn1747984120-2\emotion_time_series\前端面试情绪.json"
    # feedback = generate_feedback(audio_path, video_path, text, output_file)
    # print("生成的反馈：", feedback)

    video_path = r"D:\AllFiles\competition\soft\Screening-LLM\data\test\video\前端面试.mp4"
    output_dir = r"D:\AllFiles\competition\soft\Screening-LLM\data\test\emotion_time_series.json"
    extract_video_emotion_time_series(video_path, output_dir)