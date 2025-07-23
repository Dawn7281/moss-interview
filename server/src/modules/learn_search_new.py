import json
import os

import requests
from dotenv import load_dotenv

from src.utils.xfyun_chat import XFYunChat

# 设置全局代理
# os.environ["http_proxy"] = "http://127.0.0.1:7890"
# os.environ["https_proxy"] = "http://127.0.0.1:7890"


def google_cse_search(query, max_results=10):
    load_dotenv()
    API_KEY = os.getenv("GOOGLE_API_KEY")
    CX = os.getenv("GOOGLE_CSE_ID")
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CX,
        "q": query,
        "num": max_results,
    }
    try:
        proxies = {
            "http": "http://127.0.0.1:7890",
            "https": "http://127.0.0.1:7890"
        }
        resp = requests.get(url, params=params,proxies=proxies)
        data = resp.json()
    except Exception as e:
        print(f"请求异常: {e}")
        return []

    #     # 打印完整返回内容，方便排查
    # print("API返回内容：")
    # print(json.dumps(data, indent=2, ensure_ascii=False))

    # 检查是否有错误字段
    if "error" in data:
        error = data["error"]
        print(f"API返回错误: 代码 {error.get('code')}，消息: {error.get('message')}")
        return []

    results = []
    if "items" in data:
        for item in data["items"]:
            results.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet"),
            })

    print(f"搜索关键词：{query}，找到 {len(results)} 条结果")
    return results

def llm_recon(keyword, content_summary):
    # 1. 读取.env中的讯飞星火API信息
    load_dotenv()
    SPARK_API_KEY = os.getenv("XFYUN_API_KEY")
    SPARK_API_SECRET = os.getenv("XFYUN_API_SECRET")
    SPARK_APP_ID = os.getenv("XFYUN_APPID")

    # 2. 初始化讯飞星火聊天实例
    search_chat = XFYunChat(
        appid=SPARK_APP_ID,
        api_key=SPARK_API_KEY,
        api_secret=SPARK_API_SECRET,
        system_prompt="你是一个专业的学习资源推荐助手，能够帮助用户找到优质的学习资料。"
    )

    analysis_prompt = f"""
    你是一个专业的学习资源推荐助手，善于分析搜索结果并对学习资源进行分类整理。

    🎯【任务目标】：
    请根据以下详细的搜索结果内容，围绕关键词 **"{keyword}"**，对下方搜索结果进行分类整理，并在某些分类资源稀缺时适当补充你已知的优质资料。

    🔍【搜索结果说明】：
    这是一个 JSON 数组，每条格式如下：
    {{
      "title": "网页标题",
      "link": "网页链接",
      "snippet": "网页简要描述"
    }}

    【搜索结果内容】：
    {content_summary}
    
    📚【推荐策略】：
    1. 优先推荐上面搜索结果中的优质资源
    2. 你也可以推荐其他你知道的优质学习资源，但要确保链接真实有效
    3. 推荐的资源应该涵盖不同的学习平台和形式

    📚【推荐分类】（按需归类）：
    1. 视频课程（如 B站、YouTube、腾讯课堂、Coursera 等）
    2. 学习文档（如官方文档、技术博客、教程站点等）
    3. 实战项目 / 开源代码（如 GitHub 项目）
    4. 其他学习平台或社区（如 CSDN、知乎、掘金、LeetCode）

    📌【任务要求】：
    1. **保留所有搜索结果中的内容**，不删除不遗漏，逐条分析每个搜索结果的具体内容，包括标题、描述并进行归类。
    2. 每条资源按如下格式整理：
       - `name`: 简洁标题（取自 `title`）
       - `desc`: 根据 `snippet` 精炼内容、说明价值
       - `url`: 对应 `link`
    3. 一条内容可归入多个分类（如是视频课程也有代码），可重复归类。
    4. **每个分类必须至少有 2 条资源**，如搜索结果不足，请你适当补充高质量资料。
    5. 每个分类下推荐 3-6 个资源，格式清晰，避免重复，对每个资源的描述要具体且有价值。. 
    5. 避免重复（如链接完全一致时只出现一次，但可多类归属）。

    📦【输出格式】（标准 JSON）：
    {{
       "video_courses": [
        {{
          "name": "资源名称",
          "desc": "内容特点和适用人群",
          "url": "真实有效链接",
        }},
        ...
      ],
      "learning_docs": [...],
      "projects": [...],
      "other_platforms": [...]
    }}

    ⚠️ 注意事项：
    - 不删除搜索结果中的任何资源；
    - 所有分类字段不可为空，每类至少2条；
    - JSON 可解析，字段名一致；
    - URL 必须真实有效，若链接已失效请注明；
    - 分类要精准，不混淆用途；

    请对下方搜索结果开始分类整理并补充资料（如有需要）：
    """

    recommendations = search_chat.chat(analysis_prompt)

    return recommendations

from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import json



def check_url(item):
    """检查单个URL是否有效，返回 (是否保留, item)"""
    try:
        PROXIES = {
            "http": "http://127.0.0.1:7890",
            "https": "http://127.0.0.1:7890"
        }
        response = requests.head(item["url"], timeout=3, proxies=PROXIES)
        if response.status_code == 200:
            return True, item
        else:
            print(f"⚠️ 删除无效链接: {item['url']} (状态码: {response.status_code})")
            return False, item
    except Exception as e:
        print(f"⚠️ 删除无效链接: {item['url']} (异常: {str(e)})")
        return False, item

def move_error_llm(recommendations, max_threads=4):
    try:
        if isinstance(recommendations, str):
            json_start = recommendations.find('{')
            json_end = recommendations.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                json_str = recommendations[json_start:json_end]
                parsed_result = json.loads(json_str)

                cleaned_result = {}
                total_removed = 0

                for category_name, category_items in parsed_result.items():
                    if isinstance(category_items, list):
                        cleaned_items = []
                        # 多线程检查 URL
                        with ThreadPoolExecutor(max_workers=max_threads) as executor:
                            futures = {
                                executor.submit(check_url, item): item
                                for item in category_items if isinstance(item, dict) and 'url' in item
                            }

                            for future in as_completed(futures):
                                keep, item = future.result()
                                if keep:
                                    cleaned_items.append(item)
                                else:
                                    total_removed += 1

                        cleaned_result[category_name] = cleaned_items
                    else:
                        cleaned_result[category_name] = category_items

                if total_removed > 0:
                    print(f"共删除了 {total_removed} 个无效链接")

                # 返回清理后的 JSON 字符串
                return json.dumps(cleaned_result, ensure_ascii=False, indent=2)
            else:
                return recommendations
        else:
            return recommendations
    except json.JSONDecodeError:
        print("JSON解析失败，返回原始结果")
        return recommendations

def learn_search(query):
    results = google_cse_search(query)
    for result in results:
        print(f"标题: {result['title']}\n链接: {result['link']}\n描述: {result['snippet']}\n")
    recommendations_json = llm_recon(keyword=query, content_summary=json.dumps(results, ensure_ascii=False))
    new_recommendations_json = move_error_llm(recommendations_json, max_threads=4)
    print(new_recommendations_json)

    return new_recommendations_json

if __name__ == "__main__":
    query = input("请输入搜索关键词：")
    learn_search(query)