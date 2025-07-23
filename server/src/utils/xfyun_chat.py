
import json
import websocket
import ssl
import _thread as thread
import fitz
from src.utils.resume_parser import *
from src.utils.xfyun_base import XFYunBase

class XFYunChat:
    def __init__(self, appid, api_key, api_secret, system_prompt="", cv_path=None):
        self.base = XFYunBase(appid, api_key, api_secret)
        self.system_prompt = system_prompt
        self.message_history = []
        self.document = None
        if cv_path:
            # self.document = self._process_pdf(cv_path)
            self.document = parse_resume(cv_path)
            if self.document:
                self.message_history.append({
                    "role": "system",
                    "content": f"CV Content:\n{self.document}\n\nSystem Instructions:\n{system_prompt}"
                })
            else:
                self.message_history.append({
                    "role": "system",
                    "content": system_prompt
                })

    def _process_pdf(self, pdf_path):
        try:
            doc = fitz.open(pdf_path)
            extracted_text = ""
            for page_num in range(doc.page_count):
                page = doc[page_num]
                blocks = page.get_text("blocks")
                for block in blocks:
                    text = block[4].strip()
                    if text:
                        if block[0] < 200 and block[3] > 12:
                            extracted_text += f"\n\n## {text}\n"
                        else:
                            extracted_text += f"{text} "
            return extracted_text
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            return ""

    def chat(self, prompt):
        response = []
        ws_url = self.base.create_url()

        def on_message(ws, message):
            result = json.loads(message)
            if result["header"]["code"] != 0:
                print(f'Error: {result["header"]["code"]} - {result["header"]["message"]}')
                ws.close()
                return

            choices = result["payload"]["choices"]
            status = choices["status"]
            content = choices["text"][0]["content"]
            response.append(content)

            if status == 2:
                ws.close()

        def on_error(ws, error):
            print(f"Error: {error}")
            ws.close()

        def on_close(ws, close_status_code, close_msg):
            print("Connection closed")

        def run(ws, *args):
            data = json.dumps(self.base.gen_params( system_prompt=self.system_prompt,query=prompt))
            ws.send(data)

        def on_open(ws):
            # data = {
            #     "header": {"app_id": self.base.appid,"uid": "1234"},
            #     "parameter": {
            #         "chat": {
            #             "domain": "lite",
            #             "temperature": 0.7,
            #             "max_tokens": 2048
            #         }
            #     },
            #     "payload": {
            #         "message": {
            #             "text": [
            #                 {"role": "system", "content": self.system_prompt},
            #                 {"role": "user", "content": prompt}
            #             ]
            #         }
            #     }
            # }
            # ws.send(json.dumps(data))
            thread.start_new_thread(run, (ws,))

        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(
            ws_url,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
            on_open=on_open
        )

        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        return ''.join(response)

    # def chat_with_history_doc(self, message, history=None):
    #     # 确保系统提示词被添加
    #     if not self.message_history:
    #         self.message_history.append({
    #             "role": "system",
    #             "content": self.system_prompt
    #         })
    #         if self.document:
    #             self.message_history.append({
    #                 "role": "system",
    #                 "content": f"CV Content:\n{self.document}"
    #             })
    #
    #     # 添加用户消息
    #     self.message_history.append({
    #         "role": "user",
    #         "content": message
    #     })
    #
    #     # 构建完整上下文
    #     context = "\n".join([msg["content"] for msg in self.message_history])
    #
    #     # 获取响应
    #     response = self.chat(context)
    #
    #     # 添加助手响应
    #     if response:
    #         self.message_history.append({
    #             "role": "assistant",
    #             "content": response
    #         })
    #
    #     return response

    def chat_with_history_doc(self, message, history=None):
        """与模型对话，支持历史记录

        Args:
            message (str): 用户消息
            history (list, optional): 历史对话记录

        Returns:
            str: 模型回复
        """
        if not self.message_history:
            self.message_history.append({"role": "system", "content": self.system_prompt})

        self.message_history.append({"role": "user", "content": message})

        # print("Current message history:", self.message_history)

        # 构建完整的对话历史
        messages = []
        for msg in self.message_history:
            if msg["role"] == "system":
                messages.append({"role": "system", "content": msg["content"]})
            elif msg["role"] == "user":
                messages.append({"role": "user", "content": msg["content"]})
            elif msg["role"] == "assistant":
                messages.append({"role": "assistant", "content": msg["content"]})
        response = self.chat(str(messages[-1]["content"]))  # 只发送最后一条消息
        self.message_history.append({"role": "assistant", "content": response})

        return response

    def get_message_history(self):
        return self.message_history