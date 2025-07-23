# # src/utils/xfyun_tts.py
# import websocket
# import datetime
# import hashlib
# import base64
# import hmac
# import json
# from urllib.parse import urlparse
# import time
# from threading import Event
#
# class XFyunTTS:
#     def __init__(self, appid, api_key, api_secret):
#         self.APPID = appid
#         self.APIKey = api_key
#         self.APISecret = api_secret
#         self.Host = "tts-api.xfyun.cn"
#
#     def create_url(self):
#         """创建鉴权URL"""
#         url = 'wss://tts-api.xfyun.cn/v2/tts'
#         # 生成RFC1123格式的时间戳
#         now = datetime.datetime.now()
#         date = now.strftime('%a, %d %b %Y %H:%M:%S %Z')
#
#         # 拼接字符串
#         signature_origin = f"host: {self.Host}\ndate: {date}\nGET /v2/tts HTTP/1.1"
#
#         # hmac-sha256加密
#         signature_sha = hmac.new(self.APISecret.encode('utf-8'),
#                                signature_origin.encode('utf-8'),
#                                digestmod=hashlib.sha256).digest()
#         signature_sha_base64 = base64.b64encode(signature_sha).decode()
#
#         authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
#         authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode()
#
#         # 将请求的鉴权参数组合为字典
#         v = {
#             "authorization": authorization,
#             "date": date,
#             "host": self.Host
#         }
#         # 拼接鉴权参数，生成url
#         url = url + '?' + '&'.join([f'{k}={v}' for k, v in v.items()])
#         return url
#
#     def convert(self, text):
#         """将文本转换为音频数据"""
#         audio_data = bytearray()
#         receive_finished = Event()
#
#         def on_message(ws, message):
#             try:
#                 message = json.loads(message)
#                 code = message["code"]
#                 if code != 0:
#                     print(f'Error: {code}, {message.get("message", "")}')
#                     ws.close()
#                     return
#
#                 data = message["data"]
#                 audio = base64.b64decode(data["audio"])
#                 audio_data.extend(audio)
#
#                 if message["data"]["status"] == 2:
#                     ws.close()
#                     receive_finished.set()
#
#             except Exception as e:
#                 print(f"Error processing message: {e}")
#                 ws.close()
#
#         def on_error(ws, error):
#             print(f"Error: {error}")
#             receive_finished.set()
#
#         def on_close(ws, close_status_code, close_msg):
#             receive_finished.set()
#
#         ws = websocket.WebSocketApp(
#             self.create_url(),
#             on_message=on_message,
#             on_error=on_error,
#             on_close=on_close
#         )
#
#         def run():
#             business_params = {
#                 "aue": "raw",
#                 "auf": "audio/L16;rate=16000",
#                 "vcn": "aisjiuxu",  # 发音人
#                 "tte": "utf8",
#                 "speed": 50,        # 语速，可选值：[0-100]，默认50
#                 "volume": 50,       # 音量，可选值：[0-100]，默认50
#                 "pitch": 50,        # 音高，可选值：[0-100]，默认50
#                 "bgs": 0,          # 是否有背景音乐，0表示无，1表示有
#             }
#
#             data = {
#                 "common": {"app_id": self.APPID},
#                 "business": business_params,
#                 "data": {
#                     "status": 2,
#                     "text": base64.b64encode(text.encode('utf-8')).decode('utf-8')
#                 }
#             }
#             ws.run_forever()
#             ws.send(json.dumps(data))
#
#         import threading
#         threading.Thread(target=run).start()
#         receive_finished.wait()
#         return bytes(audio_data)


import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import os

class XFyunTTS:
    def __init__(self, appid, api_key, api_secret):
        self.APPID = appid
        self.APIKey = api_key
        self.APISecret = api_secret
        self.Host = "ws-api.xfyun.cn"

    def create_url(self):
        """创建鉴权URL"""
        url = 'wss://tts-api.xfyun.cn/v2/tts'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.Host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"

        # hmac-sha256加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'),
                               signature_origin.encode('utf-8'),
                               digestmod=hashlib.sha256).digest()
        signature_sha_base64 = base64.b64encode(signature_sha).decode()

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode()

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.Host
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        return url

    def convert(self, text):
        """将文本转换为音频数据"""
        audio_data = bytearray()
        finished = False

        def on_message(ws, message):
            nonlocal finished
            try:
                message = json.loads(message)
                code = message["code"]
                if code != 0:
                    print(f'Error: {code}, {message.get("message", "")}')
                    ws.close()
                    return

                audio = base64.b64decode(message["data"]["audio"])
                audio_data.extend(audio)

                status = message["data"]["status"]
                if status == 2:
                    finished = True
                    ws.close()

            except Exception as e:
                print(f"Error processing message: {e}")
                finished = True
                ws.close()

        def on_error(ws, error):
            nonlocal finished
            print(f"Error: {error}")
            finished = True

        def on_close(ws, close_status_code, close_msg):
            nonlocal finished
            print("### Connection closed ###")
            finished = True

        def on_open(ws):
            def run(*args):
                business_params = {
                    "aue": "raw",
                    "auf": "audio/L16;rate=16000",
                    "vcn": "xiaoyan",
                    "tte": "utf8"
                }

                data = {
                    "common": {"app_id": self.APPID},
                    "business": business_params,
                    "data": {
                        "status": 2,
                        "text": str(base64.b64encode(text.encode('utf-8')), "UTF8")
                    }
                }
                ws.send(json.dumps(data))

            thread.start_new_thread(run, ())

        websocket.enableTrace(False)
        ws_url = self.create_url()
        ws = websocket.WebSocketApp(
            ws_url,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
            on_open=on_open
        )

        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

        while not finished:
            pass

        return bytes(audio_data)