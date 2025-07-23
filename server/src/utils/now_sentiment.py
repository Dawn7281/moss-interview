import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"  # ✅ 禁用 oneDNN
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"   # ✅ 静音日志（可选）
import cv2
import numpy as np
from fer import FER
import json
import os

class RealTimeEmotionAnalyzer:
    def __init__(self):
        self.detector = FER(mtcnn=True)
        self.results = []
        self.fps = 25
        self.frame_idx = 0

    def set_fps(self, fps):
        self.fps = fps

    def map_to_interview_emotions(self, emotions):
        return {
            "confidence": emotions["happy"] * 0.7 + emotions["neutral"] * 0.3,
            "nervousness": emotions["fear"] * 0.6 + emotions["sad"] * 0.3 + emotions["neutral"] * -0.2,
            "frustration": emotions["sad"] * 0.6 + emotions["disgust"] * 0.4,
            "attentiveness": emotions["neutral"],
            "confusion": emotions["surprise"] * 0.8 + emotions["fear"] * 0.2
        }

    def update_with_frame(self, frame, time):
        results = self.detector.detect_emotions(frame)
        # timestamp = self.frame_idx / self.fps
        out = {}

        if results:
            emotions = results[0]["emotions"]
            interview_emotions = self.map_to_interview_emotions(emotions)

            self.results.append({
                "frame": self.frame_idx,
                "time_sec": time,
                "interview_emotions": interview_emotions
            })

            print({
                "frame": self.frame_idx,
                "time_sec": time,
                "interview_emotions": interview_emotions
            })

            out = interview_emotions

        self.frame_idx += 1

        return out

    def get_avg_emotions(self):
        if not self.results:
            return {}
        keys = self.results[0]["interview_emotions"].keys()
        return {
            k: float(np.mean([r["interview_emotions"][k] for r in self.results]))
            for k in keys
        }

    def get_downsampled_time_series(self, max_points=100):
        total = len(self.results)
        if total == 0:
            return []

        step = max(1, total // max_points)
        sampled = self.results[::step]

        line_chart_data = [
            {
                "time": round(item["time_sec"], 2),
                **item["interview_emotions"]
            }
            for item in sampled
        ]
        return line_chart_data

# ===============================
# 🚀 本地测试主程序
# ===============================
def test_on_video(video_path, save_json="emotion_series.json"):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("无法打开视频")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    analyzer = RealTimeEmotionAnalyzer()
    analyzer.set_fps(fps)

    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"视频总帧数：{total}, FPS: {fps}")

    frame_gap = 25  # 每隔多少帧处理一次，模拟“前端不发每一帧”

    for i in range(0, total, frame_gap):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if not ret:
            break
        analyzer.update_with_frame(frame, i / fps)
        print(f"分析帧 {i} ...")

    cap.release()

    # 打印并保存结果
    avg = analyzer.get_avg_emotions()
    series = analyzer.get_downsampled_time_series(max_points=50)

    print("\n📊 平均interview_emotions：", json.dumps(avg, indent=2))
    print("📈 Downsampled 时间序列情绪点数：", len(series))

    # 保存为 JSON 文件供可视化使用
    with open(save_json, "w", encoding="utf-8") as f:
        json.dump(series, f, indent=2, ensure_ascii=False)

    print(f"情绪时间序列已保存到：{save_json}")

# ===============================
# ⏯ 运行测试（替换成你的视频路径）
# ===============================
if __name__ == "__main__":
    video_path = r'..\..\data\test\video\前端面试.mp4'
    save_json = r"..\..\data\test\emotion_series.json"
    test_on_video(video_path,save_json)
