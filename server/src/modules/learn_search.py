import os
import time
import json
from dotenv import load_dotenv
from googlesearch import search
from src.utils.xfyun_chat import XFYunChat
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import re

# 设置全局代理
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

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

def fetch_url_content(url, timeout=5):
    """获取URL内容并提取关键信息"""
    try:
        proxies = {
            "http": "http://127.0.0.1:7890",
            "https": "http://127.0.0.1:7890"
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout,proxies=proxies)
        response.raise_for_status()
        
        # 提取标题
        title_match = re.search(r'<title[^>]*>(.*?)</title>', response.text, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else "未知标题"
        
        # 提取描述
        desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', response.text, re.IGNORECASE)
        description = desc_match.group(1).strip() if desc_match else ""
        
        # 提取正文内容（简化版）
        content = re.sub(r'<[^>]+>', '', response.text)
        content = re.sub(r'\s+', ' ', content).strip()
        content = content[:500]  # 只取前500字符
        
        return {
            'title': title,
            'description': description,
            'content': content,
            'url': url
        }
    except Exception as e:
        return {
            'title': f"无法访问: {url}",
            'description': f"访问失败: {str(e)}",
            'content': "",
            'url': url
        }

def fetch_url_content_with_progress(args):
    """带进度显示的URL内容获取函数"""
    url, index, total = args
    print(f"分析第 {index}/{total} 个链接: {url}")
    result = fetch_url_content(url)
    return result

def google_search_with_retry(query, max_results=10, max_retries=3):
    """使用Google搜索，带重试机制"""
    for attempt in range(max_retries):
        try:
            print(f"Google搜索尝试 {attempt + 1}/{max_retries}...")
            results = []

            # 使用google-search-python进行搜索
            search_query = f"{query} 学习教程 视频 课程 在线学习"
            for url in search(search_query, num_results=max_results, lang="zh"):
                results.append(url)

            if results:
                return results[:15]  # 返回前15个结果用于内容分析

        except Exception as e:
            print(f"Google搜索失败 (尝试 {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                print("等待 3 秒后重试...")
                time.sleep(3)
            else:
                print("Google搜索都失败了，使用备用方案...")
                return []

    return []

# 4. 备用搜索（无搜索服务时提供常规平台）
def fallback_search(keyword):
    return f"""⚠️ 当前网络环境限制了搜索服务。以下是关于"{keyword}"的一些常见学习平台推荐：

1. [慕课网](https://www.imooc.com) - 提供大量编程/职场类中文课程
2. [哔哩哔哩](https://www.bilibili.com) - 搜索"{keyword} 教程"获取视频资源
3. [Coursera](https://www.coursera.org) - 海量英语在线大学课程
4. [GitHub](https://github.com/search?q={keyword}) - 查找相关开源学习项目
5. [Stack Overflow](https://stackoverflow.com/search?q={keyword}) - 搜索技术问答
"""

def find_learning_resources(keyword):
    """查找学习资源的简单版本"""
    print(f"正在搜索关于 '{keyword}' 的学习资源...")
    
    # 1. 搜索相关资源（使用Google搜索）
    search_urls = google_search_with_retry(keyword)
    
    if not search_urls:
        print("搜索失败，使用备用方案...")
        fallback_result = fallback_search(keyword)
        print(f"\n【学习资源推荐】\n{fallback_result}")
        return fallback_result
    
    print(f"找到 {len(search_urls)} 个搜索结果，正在并行分析内容...")
    
    # 2. 使用多线程并行获取每个URL的内容信息
    url_contents = []
    
    # 准备参数
    args_list = [(url, i+1, len(search_urls)) for i, url in enumerate(search_urls)]
    
    # 使用线程池并行处理
    with ThreadPoolExecutor(max_workers=4) as executor:
        # 提交所有任务
        future_to_url = {executor.submit(fetch_url_content_with_progress, args): args for args in args_list}
        
        # 收集结果
        for future in as_completed(future_to_url):
            try:
                result = future.result()
                url_contents.append(result)
            except Exception as e:
                url, index, total = future_to_url[future]
                print(f"处理链接 {index} 时出错: {e}")
                url_contents.append({
                    'title': f"处理失败: {url}",
                    'description': f"错误: {str(e)}",
                    'content': "",
                    'url': url
                })
    
    # 3. 构建详细的分析提示，提供参考但不限制
    content_summary = ""
    valid_urls = []  # 记录有效的URL
    
    for i, content in enumerate(url_contents, 1):
        # 只处理能成功获取内容的链接
        if "无法访问" not in content['title'] and "处理失败" not in content['title'] and content['content']:
            valid_urls.append(content['url'])
            content_summary += f"""
                链接 {len(valid_urls)}: {content['url']}
                标题: {content['title']}
                描述: {content['description']}
                内容摘要: {content['content'][:200]}...
                ---
            """
    
    print(f"成功分析 {len(valid_urls)} 个有效链接，正在生成推荐...")
    
    # 4. 让LLM分析搜索结果并推荐
    analysis_prompt = f"""
        你是一个专业的学习资源推荐助手，善于分析搜索结果并对学习资源进行分类整理。

        请根据以下详细的搜索结果内容，围绕"{keyword}"这一主题，筛选和分类推荐高质量的学习资源。

        🔍【搜索结果参考】：
        {content_summary}

        📚【推荐策略】：
        1. 优先推荐上面搜索结果中的优质资源
        2. 你也可以推荐其他你知道的优质学习资源，但要确保链接真实有效
        3. 推荐的资源应该涵盖不同的学习平台和形式

        📚【你的任务】：
        1. 仔细分析每个链接的具体内容，包括标题、描述和内容摘要
        2. 将这些资源划分到以下 3~4 类中：
        - 视频课程（如 B站、YouTube、腾讯课堂、Coursera等）
        - 学习文档（如 菜鸟教程、W3School、官方文档、掘金等）
        - 实战项目 / 开源代码（如 GitHub 项目、教程仓库）
        - 其他有帮助的学习平台或社区

        3. 每个分类下推荐 3-6 个资源，格式清晰，避免重复
        4. 对每个资源的描述要具体且有价值

        🧠 请以以下 **JSON 格式** 返回：

        {{
        "video_courses": [
            {{
            "name": "资源名称",
            "desc": "具体说明这个资源的特点和价值",
            "url": "真实有效的链接"
            }},
            ...
        ],
        "learning_docs": [...],
        "projects": [...],
        "other_platforms": [...]
        }}

        ⚠️ 注意：
        - 确保 JSON 格式正确，可以被解析
        - 所有URL必须是真实有效的链接
        - 描述要具体，说明资源的特点和适用人群
        - 没有的分类可以省略，但不要返回 null
        - 可以推荐搜索结果之外的优质资源

"""

    recommendations = search_chat.chat(analysis_prompt)
    
    # 5. 验证返回的链接并过滤无效链接
    try:
        # 尝试解析JSON
        if isinstance(recommendations, str):
            # 提取JSON部分
            json_start = recommendations.find('{')
            json_end = recommendations.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                json_str = recommendations[json_start:json_end]
                parsed_result = json.loads(json_str)
                
                # 验证所有URL并删除无效的
                cleaned_result = {}
                total_removed = 0
                
                for category_name, category_items in parsed_result.items():
                    if isinstance(category_items, list):
                        cleaned_items = []
                        for item in category_items:
                            if isinstance(item, dict) and 'url' in item:
                                # 检查URL是否在有效列表中（优先）或尝试访问验证
                                if item['url'] in valid_urls:
                                    cleaned_items.append(item)
                                else:
                                    # 对于不在搜索结果中的链接，尝试快速验证
                                    try:
                                        response = requests.head(item['url'], timeout=3)
                                        if response.status_code == 200:
                                            cleaned_items.append(item)
                                        else:
                                            print(f"⚠️ 删除无效链接: {item['url']} (状态码: {response.status_code})")
                                            total_removed += 1
                                    except:
                                        print(f"⚠️ 删除无效链接: {item['url']} (无法访问)")
                                        total_removed += 1
                            else:
                                cleaned_items.append(item)
                        cleaned_result[category_name] = cleaned_items
                    else:
                        cleaned_result[category_name] = category_items
                
                if total_removed > 0:
                    print(f"共删除了 {total_removed} 个无效链接")
                
                # 将清理后的结果转换回JSON字符串
                recommendations = json.dumps(cleaned_result, ensure_ascii=False, indent=2)
                
                return recommendations
            else:
                return recommendations
        else:
            return recommendations
    except json.JSONDecodeError:
        print("JSON解析失败，返回原始结果")
        return recommendations

# 5. 主程序
if __name__ == "__main__":
    keyword = input("请输入你要查找的学习主题关键词：")
    result = find_learning_resources(keyword)
    print("\n【学习资源推荐】\n", result) 