import os
from dotenv import load_dotenv
from src.utils.xfyun_chat import XFYunChat  # 请根据项目结构调整路径

# 你原始的 prompt 模板，保持不变
accuracy_prompt_template = """\
你是一位具备教学与专业背景的面试评估专家，任务是根据面试过程中候选人的回答进行准确性分析。

你将获得以下信息：
- 当前问题
- 当前回答

请依据上述内容，从以下维度对当前回答进行结构化评估，仅聚焦当前问题，忽略未提及内容。

---

【输出要求】：

请按照以下格式用自然语言输出，不使用 JSON，仅使用清晰的结构化段落格式：

【准确率】：用整数形式给出百分比，例如 85%

【反馈】：简洁、专业地描述当前回答中正确与不足之处，仅聚焦当前问题，不展开无关内容

【改进建议】：
- 每条建议前加破折号“–”，每条为一行
- 指出回答中需要补充或改进的要点
- 可包括术语、逻辑、结构、举例、语言等方面

---

【示例输出】：

【准确率】：85%

【反馈】：候选人基本理解了面试官的问题，准确解释了内存泄漏的原因，但忽略了因闭包造成的引用问题。

【改进建议】：
– 补充闭包导致的内存泄漏情况
– 简要说明如何手动释放资源

---

注意事项：
- 只评估当前回答涉及的内容，未提及的不扣分
- 忽略知识截止时间，假设你拥有最新知识
- 输出格式清晰、结构分明
- 不要额外输出说明文字或 JSON 格式
"""


def format_qa_pair(question, answer, feedback):
    return f"Question: {question}\nAnswer: {answer}\nFeedback: {feedback}".strip()

def build_user_input(question, answer):
    user_input = (
        f"Current question:\n{question}\n\n"
        f"Current answer:\n{answer}\n"
    )
    return user_input

def process_qa_pair(chat):
    try:
        # 只加载一次 .env 文件，先加载父目录的 .env，再加载当前目录的（如果有的话）
        load_dotenv(os.path.join(os.path.dirname(os.getcwd()), ".env"))
        load_dotenv()

        # 初始化你的 XFYunChat 模型（带 system_prompt）
        acc_feedback_model = XFYunChat(
            appid=os.getenv("XFYUN_APPID"),
            api_key=os.getenv("XFYUN_API_KEY"),
            api_secret=os.getenv("XFYUN_API_SECRET"),
            system_prompt=accuracy_prompt_template
        )

        print(f"处理 Q&A pair:\nQuestion: {chat['interviewer']}\nAnswer: {chat['candidate']}")
        question = chat['interviewer']
        answer = chat['candidate']
        user_input = build_user_input(question, answer)
        # 调用模型
        response = acc_feedback_model.chat(user_input)
        feedback = response.strip()

        # 保存反馈并拼接上下文
        chat['feedback'] = feedback
        print(f"Feedback: {feedback}")

        return feedback

    except Exception as e:
        print(f"Error processing Q&A pair: {str(e)}")
        raise

# 测试
if __name__ == "__main__":
    chat_log = [
        {
            'interviewer': "你提到了 GCN 和 Transformer，你能说下它们在这个任务中的作用吗？",
            'candidate': """GCN 的主要作用是建模人体关节之间的空间关系。比如手和肩的相对运动、腿部支撑时的姿态变化等，它利用邻接矩阵来编码关节的连接。

Transformer 模块更适合处理长时间序列的行为模式，比如“先起身再走出房间”这种复合行为。它的多头注意力机制可以帮助模型在所有帧之间自由建立依赖。

两者结合就能更好地建模“时-空”信息，从而提高对复杂行为的识别能力。
"""
        },
        {
            'interviewer': "这个项目的数据来自哪里？你们怎么处理的？",
            'candidate': """比赛官方提供了人体骨架点序列数据，格式是类似 (N, C, T, V)，其中 N 是样本数，C 是通道数（我们处理的是2D坐标，即x, y），T 是帧数，V 是关键点数量。

我们对数据做了一些标准化操作，比如统一帧长、填补缺失帧，并根据模态需求构建了 joint（关节）、bone（骨骼向量）、motion（速度）等不同输入分支，为后续多模态模型做准备。
"""
        }
    ]

    result = process_qa_pair(chat_log)
    # for item in result:
    #     print(f"Question: {item['interviewer']}\nAnswer: {item['candidate']}\nFeedback: {item['feedback']}\n")
