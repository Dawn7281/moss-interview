import os
import json
from dotenv import load_dotenv, find_dotenv
from src.utils.xfyun_chat import XFYunChat
from src.utils.resume_parser import *
from datetime import datetime

relate_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

FEEDBACK_FOLDER = os.path.join(relate_path, 'data/json/resume_analyse')
os.makedirs(FEEDBACK_FOLDER, exist_ok=True)

class ResumeOptimizer:
    def __init__(self, role: str,job_description: str = None):
        self.role = role
        self.job_description = job_description
        # self.system_prompt = f"""
        #     你是一名人力资源专家，擅长从技术岗位角度和HR岗位角度给出简历优化建议。请基于候选人的简历内容，针对“{self.role}”岗位，指出以下几点：
        #     1. 简历中有哪些亮点；
        #     2. 哪些内容可以补充或强化；
        #     3. 用语是否专业、清晰；
        #     4. 给出3条具体修改建议。
        #     请用中文输出建议。
        # """
        self.system_prompt = """\
        你是一位资深 HR 顾问与技术专家，将对候选人的简历进行结构化评估。你将获得以下三部分信息：

        1. 候选人简历原文（CV 内容）  
        2. 目标岗位名称  
        3. 岗位职责与要求（JD 描述）

        你的任务是从以下三个方面对候选人进行分析，并输出**结构化 JSON 格式**结果。

        ---

        【分析任务】

        一、岗位匹配度分析（matching_scores）  
        请分别对下列三个维度评分，每个维度下有三个子项：

        1. 技能匹配度（skills_match）
           - 核心技能匹配（core_skills）  
           - 技术栈覆盖（tech_stack）  
           - 项目经验相关性（project_relevance）

        2. 经验与背景契合度（experience_match）
           - 工作年限匹配（years_fit）  
           - 项目规模复杂度（project_scale）  
           - 行业背景适配性（industry_fit）

        3. 职业发展契合度（career_fit）
           - 职业路径一致性（career_path）  
           - 成长潜力（growth_potential）  
           - 职业稳定性（stability）

        每个子项和总项请给出：
        - `score`（0-100 整数）
        - `comments`（简洁评语组成的字符串数组）

        ---

        二、简历优化建议（resume_optimization）

        请输出以下字段：
        - `highlights`：简历中已有亮点（如技能、经历、奖项），字符串数组
        - `improvements_needed`：缺失或可补充内容（如项目成果细节），字符串数组
        - `expression_suggestions`：表达方式可改进点（如描述不够具体或格式问题），字符串数组

        ---

        三、最终推荐建议（final_recommendation）

        请给出：
        - `decision`：仅限于 ["推荐", "待定", "不推荐"]
        - `key_reasons`：支撑推荐判断的理由（字符串数组）
        - `suggested_actions`：下一步行动建议（字符串数组）

        ---

        【输出格式要求】

        ⚠️ 请严格输出以下 JSON 结构，各字段均不得省略、改名、合并、嵌套错位。注意字段名称必须为英文！

        ```json
        {
          "matching_scores": {
            "skills_match": {
              "score": 0,
              "details": {
                "core_skills": 0,
                "tech_stack": 0,
                "project_relevance": 0
              },
              "comments": ["..."]
            },
            "experience_match": {
              "score": 0,
              "details": {
                "years_fit": 0,
                "project_scale": 0,
                "industry_fit": 0
              },
              "comments": ["..."]
            },
            "career_fit": {
              "score": 0,
              "details": {
                "career_path": 0,
                "growth_potential": 0,
                "stability": 0
              },
              "comments": ["..."]
            }
          },
          "overall_match": 0,
          "resume_optimization": {
            "highlights": ["..."],
            "improvements_needed": ["..."],
            "expression_suggestions": ["..."]
          },
          "final_recommendation": {
            "decision": "推荐",
            "key_reasons": ["..."],
            "suggested_actions": ["..."]
          }
        }
"""
        load_dotenv(os.path.join(os.path.dirname(os.getcwd()), ".env"))
        load_dotenv()
        self.resume_improve_model = XFYunChat(
            appid=os.getenv("XFYUN_APPID"),
            api_key=os.getenv("XFYUN_API_KEY"),
            api_secret=os.getenv("XFYUN_API_SECRET"),
            system_prompt=self.system_prompt
        )

    def save_result_as_json(self,feedback_path,feedback_data):
        # Get current timestamp to use in the file name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{timestamp}.json"
        file_path = os.path.join(feedback_path, file_name)

        # Write the JSON data into the file with UTF-8 encoding
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(feedback_data, f, ensure_ascii=False, indent=2)

        print(f"Result saved to: {file_path}")

    def optimize_resume(self, resume_dict: dict,name) -> str:
        resume_text = self._format_resume(resume_dict)
        # 构建输入内容
        input_content = {
            "resume": resume_text,
            "job_role": self.role,
            "job_description": self.job_description
        }

        # 拼接 prompt
        full_prompt = f"""
        请根据以下简历内容、目标岗位、岗位职责进行结构化评估：

        【简历内容】
        {resume_text}

        【目标岗位】
        {self.role}

        【岗位职责与要求】
        {self.job_description}

        请根据系统提示中的格式要求完成输出。
        """

        response = self.resume_improve_model.chat(full_prompt)
        if response is None:
            print("没有收到模型的响应，请检查模型配置或网络连接。")
            return None
        else:
            feedback_path = os.path.join(FEEDBACK_FOLDER, name)
            os.makedirs(feedback_path, exist_ok=True)
            self.save_result_as_json(feedback_path,response)
        print("🔍 简历优化建议：\n", response)
        # return self.parse_feedback_to_json(response)
        return response
    def _format_resume(self, resume_dict: dict) -> str:
        """将 dict 转换成格式清晰的文本，便于 LLM 理解"""
        parts = []
        for key, value in resume_dict.items():
            if isinstance(value, list):
                value_str = "\n  - " + "\n  - ".join(map(str, value))
            else:
                value_str = str(value)
            parts.append(f"{key}:\n{value_str}")
        return "\n\n".join(parts)

    def parse_feedback_to_json(self, text):
        """将反馈文本解析为JSON格式"""
        lines = text.strip().split('\n')
        feedback_data = []

        current_section = None
        current_points = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 检查是否是主要分类（1. 2. 3.）
            if line[0].isdigit() and line[1] == '.':
                # 保存之前的分类
                if current_section:
                    feedback_data.append({
                        "point": current_section,
                        "content": current_points.copy()
                    })

                # 开始新分类
                current_section = line[2:].strip().rstrip('：')
                current_points = []

            # 检查是否是子项（以 - 开头）
            elif line.startswith('-'):
                point = line[1:].strip()
                current_points.append(point)

        # 添加最后一个分类
        if current_section:
            feedback_data.append({
                "point": current_section,
                "content": current_points
            })

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{timestamp}.json"
        file_path = os.path.join(FEEDBACK_FOLDER, file_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(feedback_data, f, ensure_ascii=False, indent=2)

        return feedback_data

if __name__ == "__main__":
    json_path = r"D:\AllFiles\competition\soft\Screening-LLM\data\cvs\web前端开发工程师-active.docx"
    name = "杨璐雨"
    cv_json = parse_resume(json_path)
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
    optimizer = ResumeOptimizer(role,job_description)
    advice = optimizer.optimize_resume(cv_json, name)
    # print(advice)
