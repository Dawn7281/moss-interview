
import os

from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_core.runnables import Runnable
from langchain.embeddings import HuggingFaceEmbeddings

from src.utils.webscraper import WebScraper
from src.utils.xfyun_chat import XFYunChat  # 修改路径根据你项目结构来

# 讯飞星火适配器
class XFYunChatAdapter(Runnable):
    def __init__(self, xfyun_chat):
        self.xfyun_chat = xfyun_chat

    def invoke(self, messages):
        if isinstance(messages, str):
            prompt = messages
        else:
            prompt = "\n".join([msg["content"] for msg in messages])
        return {"content": self.xfyun_chat.chat(prompt)}

embedding_model = HuggingFaceEmbeddings(model_name="../../model/all-MiniLM-L6-v2")
def format_qa_pair(question, answer, feedback):
    return f"Question: {question}\nAnswer: {answer}\nFeedback: {feedback}".strip()

def process_qa_pair(chat_log):
    try:
        # 加载 .env
        parent_folder_path = os.path.dirname(os.getcwd())
        dotenv_path = os.path.join(parent_folder_path, ".env")
        load_dotenv(dotenv_path)

        # 初始化讯飞星火
        xfyun_chat = XFYunChat(
            appid=os.getenv("XFYUN_APPID"),
            api_key=os.getenv("XFYUN_API_KEY"),
            api_secret=os.getenv("XFYUN_API_SECRET"),
        )
        llm = XFYunChatAdapter(xfyun_chat)

        # 子查询 prompt
        prompt_decomposition = ChatPromptTemplate.from_template(
            """You are a helpful assistant that generates multiple sub-queries related to an answer by an interview candidate. 
            You will be provided the original question for context. The goal is to find the accuracy of the answer. 
            Generate multiple search queries related to: {answer} 
            Output (2 queries):"""
        )

        def generate_queries(input_dict):
            prompt = prompt_decomposition.format(**input_dict)
            response = llm.invoke(prompt)
            return response["content"].split("\n")

        documents = []

        # 抓取内容
        for qa_pair in chat_log:
            question = qa_pair['interviewer']
            answer = qa_pair['candidate']
            queries = generate_queries({"question": question, "answer": answer})
            print(f"search queries generated: {queries}")
            for query in queries:
                scraper = WebScraper(query, 4)
                documents.extend(scraper.search_and_scrape())

        # 文本切分
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=300, chunk_overlap=50
        )

        try:
            splits = text_splitter.split_documents(documents)
            if not splits:
                print("No documents split. Empty retriever.")
                retriever = RunnablePassthrough()
            else:
                vectorstore = Chroma.from_documents(splits, embedding=embedding_model, persist_directory="chroma_db")
                retriever = vectorstore.as_retriever()
        except Exception as e:
            print(f"Document processing error: {e}")
            retriever = RunnablePassthrough()

        # 构建准确性校验模板
        accuracy_prompt = ChatPromptTemplate.from_template("""
                Here is the question for the answer you need to check:

                \n --- \n {question} \n --- \n

                Here is the answer you need to check:

                \n --- \n {answer} \n --- \n

                Here is any available background question + answer + accuracy percentage + feedback:

                \n --- \n {q_a_pairs} \n --- \n

                Here is additional context relevant to the question:

                \n --- \n {context} \n --- \n

                Use the above context, your own knowledge and background question + answer + accuracy percentage + feedback
                on the subject matter to get the accuracy of the answer. A percentage accuracy score and also note down the
                places that the answer was inaccurate and give feedback for those places. Keep in mind the following points
                when providing feedback:
                1. Do not mention any terminology errors in the answer. If you detect there is any errors arising from terminology
                correct it in the feedback and mention that it was due to an error in transcription and not a problem with
                the candidate. Do not deduct accuracy score because of this
                2. Do not mention any typographical errors in the answer. If you detect there is any errors arising from typography
                correct it in the feedback and mention that it was due to an error in transcription and not a problem with
                the candidate. Do not deduct accuracy score because of this.
                3. Do not mention any topics the candidate did not answer if it was not asked in the question.
                4. Do not include a summary at the end of each question answer pair.
                5. Do not consider your last knowledge update as I am feeding you with current upto date information in the context.

                """)

        rag_chain = (
            {
                "context": itemgetter("answer") | retriever if documents else RunnablePassthrough(),
                "answer": itemgetter("answer"),
                "question": itemgetter("question"),
                "q_a_pairs": itemgetter("q_a_pairs")
            }
            | accuracy_prompt
            | llm
            | StrOutputParser()
        )

        q_a_pairs = ""

        for chat in chat_log:
            question = chat['interviewer']
            answer = chat['candidate']
            feedback = rag_chain.invoke({
                "answer": answer,
                "question": question,
                "q_a_pairs": q_a_pairs
            })["content"]
            chat['feedback'] = feedback
            q_a_pairs += "\n---\n" + format_qa_pair(question, answer, feedback)

        return chat_log

    except Exception as e:
        print(f"Error processing Q&A pair: {str(e)}")
        raise

#To Test
if __name__ == "__main__":
    chat_log = [{'interviewer': "Hello! It's nice to meet you too. Thank you for taking the time to speak with me today about the Entry-Level RAG AI Engineer role. To start off, could you tell me about your experience with retrieval-augmented generation (RAG) pipelines?", 'candidate': " Yeah sure, I'd be happy to. I have a good amount of experience with retrieval augmented generated pipelines. In my current job position I developed a pipeline for web scraping a certain website which is determined by a previous step in our system. Oh my god dude. Bro, just give me a minute."}, {'interviewer': "No problem, take your time. When you're ready, could you elaborate on how you implemented the RAG pipeline in your current role? What specific technologies or frameworks did you use?", 'candidate': 'System - The candidate Ended the Interview'}]

    result = process_qa_pair(chat_log)
    print(result)