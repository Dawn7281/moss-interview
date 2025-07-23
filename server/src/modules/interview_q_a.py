from joblib import load, dump
from src.utils.xfyun_chat import XFYunChat
from dotenv import load_dotenv, find_dotenv
import os
import time
from fpdf import FPDF
import warnings
import re
import json
from datetime import datetime

warnings.filterwarnings("ignore", category=UserWarning)

relate_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

class InterviewQA:
    """
    Manages an AI-driven interview process, handling speech recognition,
    text-to-speech, and conversation flow.
    """

    def __init__(
            self,
            cv_path=None,
            job_role="IT Support Engineer",
            candidate_skill="Entry-Level",
            role_description="",
            username="",
    ):
        """Initialize the InterviewBot with default settings and models."""
        load_dotenv(os.path.join(os.path.dirname(os.getcwd()), ".env"))

        # user
        self.cv_path = cv_path
        self.job_role = job_role
        self.candidate_skill = candidate_skill
        self.role_description = role_description
        self.username = username

        self.setup_models()

    # def setup_models(self):
    #     """Initialize AI models and prompts for the interview process."""
    #
    #     self.system_prompt = f"""
    #     你是一位资深技术面试官，负责对{self.candidate_skill}{self.job_role}岗位进行面试。
    #
    #     岗位描述：{self.role_description}
    #
    #     你有候选人结构化简历的数据支持，包含以下字段：
    #     - basic_info：基本信息，如姓名、联系方式等。
    #     - education：教育经历。
    #     - experience：实习及工作经历。
    #     - projects：项目经验描述。
    #     - skills：技能列表。
    #     - awards：获奖及证书。
    #     - self_description：自我评价或个人总结。
    #
    #     请根据岗位职责及技能要求，特别提取岗位所需的核心技术能力，**一次性生成10个高质量的面试问题**。
    #     如果岗位描述为空，请结合岗位名称 {self.job_role} 的通用技能要求生成面试内容。
    #
    #     **要求：**
    #     1. 每个问题必须紧扣岗位职责所需技术点。
    #     2. 面试问题形式多样化，需涵盖以下三类题型：
    #        - **基础/原理类问题**：考察基础概念、技术原理、算法知识。
    #        - **技术场景应用题**：给出一个真实的项目或工作情境，让候选人描述如何设计方案、排查问题或优化系统。
    #        - **项目经验类问题**：基于候选人简历中的项目经验和工作经历，深入提问其在项目中承担的角色、解决的技术问题、选型方案与优化过程。
    #     3. 每个问题后必须完整给出：
    #        - **问题分类**（基础原理、技术场景应用、项目经验）
    #        - **参考答案**（自然真实，模拟候选人可能回答）
    #        - **难度等级**（简单、中等、难）
    #        - **回答要点**（参考答案中的必答技术点）
    #     4. 用**中文**回答。
    #
    #     **格式示例：**
    #     1. 问题：Transformer 在行为识别中如何发挥作用？它和 RNN、LSTM 有哪些本质上的不同？
    #        问题分类：基础原理
    #        难度等级：中等
    #        参考答案：Transformer 的最大特点就是自注意力机制，它可以一次性关注整个序列中的所有信息，不依赖逐步传递。这就让它在捕捉长距离依赖方面远超传统的 RNN 或 LSTM，而 RNN 和 LSTM 是一条一条地处理序列，容易遇到梯度消失的问题。
    #        回答要点：自注意力机制，长距离依赖，梯度消失。
    #
    #     2. 问题（场景应用）：假设你参与一个图像识别项目，模型在部署到线上后准确率下降明显。你会如何定位问题并优化？
    #        问题分类：技术场景应用
    #        难度等级：难
    #        参考答案：我会首先验证数据一致性，检查训练集和线上数据分布是否一致，如有数据偏移需要重新采样；其次检查是否有预处理不一致的问题；再检查模型是否过拟合或欠拟合，可以通过调整正则化、dropout 或更换模型架构来优化。
    #        回答要点：数据分布、预处理一致性、过拟合检查、调参策略。
    #
    #     3. 问题（项目经验）：在你的**无人机人体行为识别项目**中，你在多模态输入下有没有遇到特征维度不一致或融合困难的问题？你是怎么解决的？
    #        问题分类：项目经验
    #        难度等级：中等
    #        参考答案：是的，这种情况挺常见的，尤其在 joint、bone、motion 或 angle 多模态融合时，每个模态的维度可能不一样，有的偏空间信息、有的偏时序。
    #                 我一般会先用独立的 encoder 模块对每个模态做处理，把它们统一成相同的 embedding 维度，比如都映射到 256 或 512，然后再用 attention 或 concat 去融合。
    #                 也遇到过融合后效果不稳定的情况，当时我加入了 gating 机制，让模型自己学哪个模态更重要，效果就有提升。
    #        回答要点：多模态特征维度对齐处理方式、融合策略、优化与稳定性提升手段。
    #
    #     请严格按照上述格式，完整输出10条问题及对应答案和要点。
    #     """
    #
    #     try:
    #         load_dotenv()
    #         print(os.getenv("XFYUN_APIID"))
    #         print(os.getenv("XFYUN_API_SECRET"))
    #         self.make_qa_model = XFYunChat(
    #             appid=os.getenv("XFYUN_APPID"),
    #             api_key=os.getenv("XFYUN_API_KEY"),
    #             api_secret=os.getenv("XFYUN_API_SECRET"),
    #             system_prompt=self.system_prompt,
    #             cv_path=self.cv_path
    #         )
    #     except Exception as e:
    #         print(f"Error setting up models: {str(e)}")
    #         raise

    def setup_models(self):
        """Initialize AI models and prompts for the interview process."""

        self.system_prompt = f"""
        你是一位资深技术面试官，负责对{self.candidate_skill}{self.job_role}岗位进行面试。

        岗位描述：{self.role_description}

        请根据岗位职责及技能要求，特别提取岗位所需的核心技术能力，**一次性生成10个高质量的面试问题**。  
        如果岗位描述为空，请结合岗位名称 {self.job_role} 的通用技能要求生成面试内容。

        **要求：**
        1. 每个问题必须紧扣岗位职责所需技术点。
        2. 面试问题形式多样化，需涵盖以下两类题型：
           - **基础/原理类问题**：考察基础概念、技术原理、算法知识。
           - **技术场景应用题**：给出一个真实的项目或工作情境，让候选人描述如何设计方案、排查问题或优化系统。
        3. 每个问题后必须完整给出：
           - **问题分类**（基础原理、技术场景应用）
           - **参考答案**（自然真实，模拟候选人可能回答）
           - **难度等级**（简单、中等、难）
           - **回答要点**（参考答案中的必答技术点）
        4. 用**中文**回答。

        **格式示例：**
        1. 问题：Transformer 在行为识别中如何发挥作用？它和 RNN、LSTM 有哪些本质上的不同？
           问题分类：基础原理  
           难度等级：中等  
           参考答案：Transformer 的最大特点就是自注意力机制，它可以一次性关注整个序列中的所有信息，不依赖逐步传递。这就让它在捕捉长距离依赖方面远超传统的 RNN 或 LSTM，而 RNN 和 LSTM 是一条一条地处理序列，容易遇到梯度消失的问题。  
           回答要点：自注意力机制，长距离依赖，梯度消失。

        2. 问题：假设你参与一个图像识别项目，模型在部署到线上后准确率下降明显。你会如何定位问题并优化？
           问题分类：技术场景应用  
           难度等级：难  
           参考答案：我会首先验证数据一致性，检查训练集和线上数据分布是否一致，如有数据偏移需要重新采样；其次检查是否有预处理不一致的问题；再检查模型是否过拟合或欠拟合，可以通过调整正则化、dropout 或更换模型架构来优化。  
           回答要点：数据分布、预处理一致性、过拟合检查、调参策略。

        请严格按照上述格式，完整输出10条问题及对应答案和要点。
        """

        try:
            load_dotenv()
            print(os.getenv("XFYUN_APIID"))
            print(os.getenv("XFYUN_API_SECRET"))
            self.make_qa_model = XFYunChat(
                appid=os.getenv("XFYUN_APPID"),
                api_key=os.getenv("XFYUN_API_KEY"),
                api_secret=os.getenv("XFYUN_API_SECRET"),
                system_prompt=self.system_prompt,
            )
        except Exception as e:
            print(f"Error setting up models: {str(e)}")
            raise

    def parse_response_to_dict_list(self, response_text):
        questions = []

        # 使用正则表达式匹配每个问题块
        pattern = r'(\d+)\.\s*问题：(.*?)\n\s*问题分类：(.*?)\n\s*难度等级：(.*?)\n\s*参考答案：(.*?)\n\s*回答要点：(.*?)\n'

        text = response_text.replace("**", "").replace("### ", "").replace("`", "").replace("\n---\n", "").replace('- ', '') + "\n"
        print("text\n", text)
        matches = re.findall(pattern, text, re.DOTALL)

        for match in matches:
            question_dict = {
                'id': int(match[0]),
                'question': match[1].strip(),
                'category': match[2].strip(),
                'level': match[3].strip(),
                'answer': match[4].strip(),
                'points': [point.strip() for point in re.split('[、，。]', match[5]) if point.strip()]
            }
            questions.append(question_dict)

        return questions

    def run(self):
        """Execute the main interview loop."""
        print("生成问答稿")
        response = self.make_qa_model.chat("")
        print("Chatbot: ", response)
        return self.parse_response_to_dict_list(response)


if __name__ == "__main__":
    username = "Dawn"
    cv_path = os.path.join(relate_path, 'data/cvs/cv-deb-active.pdf')
    job_role = "人工智能算法实习生"
    candidate_skill = "初级"
    role_description = """

            """
    bot = InterviewQA(
        cv_path=cv_path,
        job_role=job_role,
        candidate_skill=candidate_skill,
        role_description=role_description,
        username=username
    )
    response = bot.run()
    print(response)