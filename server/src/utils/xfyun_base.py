from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time
import hmac
import hashlib
import base64
from urllib.parse import urlparse, urlencode
import os

# class XFYunBase:
#     def __init__(self, appid, api_key, api_secret):
#         self.appid = appid
#         self.api_key = api_key
#         self.api_secret = api_secret
#         self.gpt_url = "wss://spark-api.xf-yun.com/v1.1/chat"  # lite版本
#         # self.gpt_url = "wss://spark-api.xf-yun.com/v4.0/chat"  # 4.0ultra版本
#         self.host = urlparse(self.gpt_url).netloc
#         self.path = urlparse(self.gpt_url).path
#         self.domain = "lite"
#
#     def create_url(self):
#         # 生成RFC1123格式的时间戳
#         now = datetime.now()
#         date = format_date_time(mktime(now.timetuple()))
#
#         # 拼接字符串
#         signature_origin = "host: " + self.host + "\n"
#         signature_origin += "date: " + date + "\n"
#         signature_origin += "GET " + self.path + " HTTP/1.1"
#
#         # hmac-sha256加密
#         signature_sha = hmac.new(
#             self.api_secret.encode('utf-8'),
#             signature_origin.encode('utf-8'),
#             digestmod=hashlib.sha256
#         ).digest()
#         signature_sha_base64 = base64.b64encode(signature_sha).decode()
#
#         authorization_origin = f'api_key="{self.api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
#         authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode()
#
#         # 组合鉴权参数
#         v = {
#             "authorization": authorization,
#             "date": date,
#             "host": self.host
#         }
#         # 生成url
#         url = self.gpt_url + '?' + urlencode(v)
#         return url


class XFYunBase(object):
    # 初始化
    def __init__(self, appid, api_key, api_secret):
        self.appid = appid
        self.api_key = api_key
        self.api_secret = api_secret
        # self.gpt_url = "wss://spark-api.xf-yun.com/v1.1/chat"
        self.gpt_url = "wss://spark-api.xf-yun.com/v3.5/chat"
        # self.gpt_url = "wss://spark-api.xf-yun.com/v4.0/chat"
        self.host = urlparse(self.gpt_url).netloc
        self.path = urlparse(self.gpt_url).path
        # self.domain = "lite"
        self.domain = "generalv3.5"
        # self.domain = "4.0Ultra"

        # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.gpt_url + '?' + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url

    def gen_params(self, system_prompt,query):
        """生成请求参数"""
        data = {
            "header": {
                "app_id": self.appid,
                "uid": "1234"
            },
            "parameter": {
                "chat": {
                    "domain": self.domain,
                    "temperature": 0.5,
                    "max_tokens": 4096,
                    "auditing": "default"
                }
            },
            "payload": {
                "message": {
                    "text": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": query}
                    ]
                }
            }
        }
        return data