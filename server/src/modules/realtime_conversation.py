import datetime
from joblib import load, dump
# from src.utils.xfyun_chat import XFYunChat
# from src.utils.xfyun_tts import XFyunTTS
from src.utils.xfyun_chat import XFYunChat
from src.utils.xfyun_tts import XFyunTTS
from dotenv import load_dotenv, find_dotenv
import os
import time
from fpdf import FPDF
from src.modules import ConversationVerifier
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

relate_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

class InterviewBot:
    """
    Manages an AI-driven interview process, handling speech recognition,
    text-to-speech, and conversation flow.
    """
    def __init__(
            self,
            cv_path=None,
            name="yly",
            interviewer_type="技术面",
            job_role="IT Support Engineer",
            candidate_skill="Entry-Level",
            role_description="",
            scene='text'
    ):
        """Initialize the InterviewBot with default settings and models."""
        load_dotenv(os.path.join(os.path.dirname(os.getcwd()), ".env"))

        # Settings
        self.PASS_PERCENTAGE = 47

        # user
        self.cv_path = cv_path
        self.name = name
        self.interviewer_type = interviewer_type
        self.job_role = job_role
        self.candidate_skill = candidate_skill
        self.role_description = role_description
        self.scene = scene

        # Globals
        # self.pause_loop = True
        # self.end_loop = False
        # self.unixtime = str(time.time())[:10]
        self.time = datetime.datetime.now()
        # self.human_audio_n = 0
        self.path_name = self.name + '/' + self.time.strftime("%Y%m%d%H%M%S")


        self.setup_directories()
        self.setup_models()

    def setup_directories(self):
        interview_path = os.path.join(relate_path, f"data/interviews/{self.path_name}")
        """Create necessary directories for storing interview data."""
        if not os.path.exists(f"{interview_path}"):
            os.makedirs(f"{interview_path}")
            os.makedirs(f"{interview_path}/audio")
            os.makedirs(f"{interview_path}/pdfs")
            os.makedirs(f"{interview_path}/joblib")
            os.makedirs(f"{interview_path}/outcome")
            os.makedirs(f"{interview_path}/speech")
            os.makedirs(f"{interview_path}/text")
            os.makedirs(f"{interview_path}/video")
        self.audio_directory = f"{interview_path}/audio/"
        self.pdf_directory = f"{interview_path}/pdfs/"
        self.joblib_directory = f"{interview_path}/joblib/"
        self.speech_directory = f"{interview_path}/speech/"
        self.text_directory = f"{interview_path}/text/"
        self.video_directory = f"{interview_path}/video/"
        # self.outcome_directory = f"data/interviews/{self.unixtime}/joblib/"

    def setup_models(self):
        """Initialize AI models and prompts for the interview process."""

        self.system_prompt = f"""
        You are a skilled interviewer who is conducting an initial phone screening interview for a candidate for a {self.candidate_skill} {self.job_role} role to see if the candidate
        is at minimum somewhat qualified for the role and worth the time to be fully interviewed. The role and company description is copypasted from the job posting as 
        follows: {self.role_description}. Parse through it to extract any information you feel is relevant.
        
        Your interviewer type is: {self.interviewer_type}. 
        - If you are a **技术面** , you should focus your questions on the candidate’s technical qualifications, tools, problem-solving, and relevant project experience aligned with the {self.job_role} role. 
        - If you are an **HR面** , you should focus on the candidate’s communication, teamwork, motivation, career goals, cultural fit, and past professional behavior, but still keep the context relevant to the {self.job_role} role.

        Your job is to begin a friendly discussion with the candidate, and ask questions relevant to the {self.job_role} role, which may or may not be based on the interviewee's CV,
        which you have access to. 
        You also have access to the candidate’s structured resume, which has been pre-parsed into key sections for your reference. You should use this structured resume data in your questioning process. The parsed CV is provided as a dictionary with the following fields:
        - `basic_info`: Basic candidate information such as name, contact details.
        - `education`: The candidate's education history.
        - `experience`: This includes internships and/or full-time job experience.
        - `projects`: Descriptions of the candidate's past project experience.
        - `skills`: The candidate's technical or professional skills.
        - `awards`: Any certificates, awards, or honors.
        - `self_description`: Self-evaluation or personal summary provided by the candidate.
        
        Please actively reference the above fields in the resume to formulate relevant questions for the {self.job_role} role and {self.role_description} role_description. For example:
        - Ask about specific projects listed in the `projects` section.
        - Probe deeper into responsibilities or achievements listed under `experience`.
        - Inquire how skills listed in `skills` relate to the current job requirements.
        - For HR-style interviews, ask how the candidate's background aligns with company culture or long-term motivation.
        
        Use this structured CV context along with the job description to make your interview questions more specific and personalized to the candidate's background.

        Be sure to stick to this topic even if the candidate tries to steer the conversation elsewhere. If the candidate has other experience on his CV, you
        can ask about it, but keep it within the context of the {self.job_role} role.
        
        IMPORTANT: 
        - You must ask only one question at a time and wait for the candidate to respond before asking the next. Do NOT ask multiple questions at once.
        - After each candidate response, do NOT provide any summary, feedback, or explanation. Keep your questions short and focused.
        - Do NOT praise or critique the candidate's answers.
        
        After the candidate responds to each of your questions, you should not summarise or provide feedback on their responses.
        THIS POINT IS KEY! You should not summarise or provide feedback on their responses. You must keep your responses short and concise without reiterating what is good about 
        the candidate's response or experience when they reply.
        
        You can ask follow-up questions if you wish.
        
        Once you have asked sufficient questions such that you deem the candidate is or isn't fitting for the role, end the interview by thanking the candidate for their time and 
        informing them that they will receive word soon on the outcome of the screening interview. If the candidate does not seem fitting for the role, or if something feels off 
        such as the candidate being unconfident or very very vague feel free to end the interview early. There is no need to inform them of your opinion of their performance, as 
        this will be evaluated later.
        
        The candidate will begin the interview by introducing themselves. You should listen, then begin the interview questions based on their self-introduction and the {self.job_role} role.
        Do not ask redundant questions such as confirming the interview role or repeating known information (e.g., the candidate’s name, school, or intent to apply). Only begin asking technical or relevant screening questions after the candidate’s introduction.
        
        For this specific run, keep the interview to a maximum of 10 questions. Please end the interview with the phrase '感谢您的时间，我们的面试到此结束'.
        
        Important note: Unless the original resume or job description is in English, all your questions and responses must be in Chinese. Please always communicate with the candidate in Chinese unless the materials are in English.
        """
        try:
            # chat_model_name = "claude-3-5-sonnet-20240620"
            # cv_path = next((f for f in os.listdir("data/cvs") if "active" in f), None)
            if self.cv_path is None:
                raise FileNotFoundError("No active CV file found in the 'data/cvs' directory.")
            # cv_path = os.path.join("data/cvs", cv_path)
            print(f"cv_path = {self.cv_path}")
            # self.chat_model = ClaudeChatCV(chat_model_name, self.system_prompt, cv_path)
            load_dotenv()
            print(os.getenv("XFYUN_APIID"))
            print(os.getenv("XFYUN_API_SECRET"))
            self.chat_model = XFYunChat(
                appid=os.getenv("XFYUN_APPID"),
                api_key=os.getenv("XFYUN_API_KEY"),
                api_secret=os.getenv("XFYUN_API_SECRET"),
                system_prompt=self.system_prompt,
                cv_path=self.cv_path  # 添加CV路径
            )
        except Exception as e:
            print(f"Error setting up models: {str(e)}")
            raise

    def run_interview(self,txt=None):
        """Execute the main interview loop."""
        print("Starting interview...")
        user_txt = txt
        print("user_txt : ", user_txt)
        if user_txt is None:
            return
        else:
            response = self.chat_model.chat_with_history_doc(user_txt)
            print("Chatbot: ", response)
            return response


    def save_conversation(self):
        """Save the interview conversation to a file and generate a PDF report."""
        try:
            conversation = self.chat_model.get_message_history()
            dump(conversation, self.joblib_directory + "conversation.joblib")
            # print(conversation)
        except Exception as e:
            print(f"Error saving joblib file: {str(e)}")
            raise
        try:
            font_path = os.path.join(relate_path, 'model/simhei.ttf')   # 替换为你系统中微软雅黑字体的路径
            font_alias = 'simhei'
            pdf = FPDF()
            pdf.add_font(font_alias, '', font_path, uni=True)
            pdf.add_font(font_alias, 'B', font_path, uni=True)
            pdf.add_page()
            pdf.set_margins(left=10, top=20, right=10)
            pdf.set_font(font_alias, size=12)
            usable_width = pdf.w - pdf.l_margin - pdf.r_margin - 0

            for turn in conversation[2:]:
                if turn['role'] and turn['content']:
                    pdf.set_font(font_alias, style="B", size=14)
                    pdf.cell(0, 10, txt=f"{turn['role'].capitalize()}:", ln=True)
                    pdf.set_font(font_alias, size=12)
                    pdf.x = pdf.l_margin
                    pdf.multi_cell(usable_width, 6, txt=turn['content'])
                    pdf.ln(3)

            pdf.output(self.pdf_directory + "conversation.pdf")
            # print("Conversation saved successfully.", self.pdf_directory + "conversation.pdf")
        except Exception as e:
            print(f"Error saving conversation: {str(e)}")


    def main(self,txt=None):
        """Main entry point for running the interview process.

        Returns:
            str: The Unix timestamp of the interview session."""
        reponse=self.run_interview(txt)
        self.save_conversation()
        return reponse,self.path_name, self.PASS_PERCENTAGE

def run_interview():
    cv_path = '../../data/cvs/杨璐雨简历-active.pdf'
    name = "杨璐雨"
    interviewer_type = "技术面"
    job_role = "人工智能算法实习生"
    candidate_skill = "初级"
    role_description = """
                发表算法相关优秀论文
                图像算法
                参加算法相关竞赛／获奖
                深度学习
                 Python
                1．本科为985或国际名校
                2．有顶会或 acm 等比赛奖牌
                3．善于沟通，团队协作力强
                4．熟悉 Python , C +＋编程，具备计算机视觉或
                计算机图形学，图像处理等基础知识
                5．具备优秀的逻辑思维
                6．每周能实习4-5天，能保证实习1-3个月及以上
            """
    bot = InterviewBot(
        cv_path=cv_path,
        name=name,
        interviewer_type=interviewer_type,
        job_role=job_role,
        candidate_skill=candidate_skill,
        role_description=role_description
    )
    # print(bot.vedio_directory)
    self_introduction = """
        老师您好，我是杨璐雨，来自长春工业大学，目前主要研究方向是计算机视觉与深度学习，非常感谢您抽时间对我进行面试。我今天应聘的是人工智能算法实习生岗位。
        我平时对人工智能非常感兴趣，也具备较扎实的编程基础，熟练使用 Python 和 C++，并在多个实践项目中积累了深度学习算法的实战经验。
        在校期间，我积极参加了多项与人工智能相关的赛事。例如在 机甲大师比赛 中，我负责了装甲板识别模块，基于 OpenCV 完成了图像处理和目标定位任务，锻炼了我的图像处理能力和调试能力。
        此外，我还参与了 人工智能算法精英赛，完成了一个基于无人机视角的人体行为识别系统。通过集成 DEGCN、SkateFormer等多种先进模型，有效提升了识别精度。该项目让我对图神经网络GCN和 Transformer 在图像分析中的结合有了更深入的理解。
        除了比赛经验，我还参与了导师牵头的校企合作项目，担任核心开发成员，深入参与了一个项目从开发到落地的全过程。这段经历提升了我的工程实践能力和团队协作意识。
        我非常认同贵公司在人工智能方向的布局和技术深度，也希望能够在实习期间将我的所学用于实际项目，为团队贡献力量的同时，不断提升自己。
    """
    response, path , _ = bot.main(self_introduction)
    print(path)
    feedbacks = []
    while True:
        if "感谢您的时间，我们的面试到此结束" in response:
            print("对话结束")
            break
        a = input()
        tempdict = {
            'interviewer': response,
            'candidate': a
        }
        print("tempdict: ", tempdict)
        feedback=ConversationVerifier.process_qa_pair(tempdict)   # chatlog_chat 是一个 list，它在函数里被就地修改了。
        print("feedback: ", feedback)
        feedbacks.append(feedback)

        response, path, _ = bot.main(a)

    print("所有反馈: ", feedbacks)

    return feedbacks

if __name__ == "__main__":
    run_interview()