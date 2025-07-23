import os
import json
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

# 替换为你的模型文件路径
from src.utils.xfyun_chat import XFYunChat

load_dotenv(os.path.join(os.path.dirname(os.getcwd()), ".env"))
load_dotenv()

# 初始化讯飞大模型
kg_model = XFYunChat(
    appid=os.getenv("XFYUN_APPID"),
    api_key=os.getenv("XFYUN_API_KEY"),
    api_secret=os.getenv("XFYUN_API_SECRET"),
    system_prompt="你是一个专业的知识图谱专家，能够围绕任何知识点生成结构化的三元组。"
)

summary_model = XFYunChat(
    appid=os.getenv("XFYUN_APPID"),
    api_key=os.getenv("XFYUN_API_KEY"),
    api_secret=os.getenv("XFYUN_API_SECRET"),
    system_prompt="你是一个专业的总结专家，能够对一段文本进行总结,提取一个关键词。"
)


def summary_word(scene: str) -> list:
    """
    使用 LLM 提取面试反馈中的技术关键词，去掉标题等无关行。
    """
    prompt = f"""
你是一个专业的技术图谱专家，擅长从技术面试反馈中提取候选人知识薄弱点。

请从下面这段面试评语中提取出需要补强的技术关键词，包括但不限于算法名称、模块名称、技术术语、知识点等：
- 每行只输出一个关键词
- 不要加标题、不要加解释

内容如下：
{scene}
"""
    response = summary_model.chat(prompt)
    lines = [line.strip() for line in response.strip().split("\n") if line.strip()]

    # 过滤掉明显不是关键词的行（如标题）
    keywords = [
        line for line in lines
        if not any(prefix in line for prefix in ["关键词", "补强", "关键词如下", "如下"]) and len(line) < 30
    ]

    print(f"📌 提取关键词：{keywords}")
    return keywords


# 单次生成函数：围绕某个实体生成三元组
def generate_knowledge_triples(entity: str):
    prompt = f"""
请围绕“{entity}”这个知识关键词生成结构化知识图谱三元组（每行一个JSON）：
{{"h": "{entity}", "r": "关系", "t": "相关概念"}}

要求：
1. 至少8条
2. “r”可以是：属于、包含方法、优点、缺点、应用领域、涉及问题等
3. 仅输出标准 JSON 格式，不要解释说明
"""
    response = kg_model.chat(prompt)
    triples = []
    for line in response.strip().split('\n'):
        try:
            triples.append(json.loads(line.strip()))
        except:
            continue
    return triples

# 🌱 主构图逻辑：递归扩展知识图谱
# 在递归中，只扩展这些关系
ALLOWED_RELATIONS = {"属于", "是", "是一种", "属于类别", "对比方法", "包含方法", "隶属于", "类型"}

def build_knowledge_graph(seed_entity: str, max_depth: int = 2, max_nodes: int = 50):
    visited = set()
    queue = [(seed_entity, 0)]
    all_triples = []
    key = []

    while queue and len(visited) < max_nodes:
        current_entity, depth = queue.pop(0)
        if current_entity in visited or depth > max_depth:
            continue

        print(f"🌱 正在扩展：{current_entity} (深度：{depth})")
        if depth <= 1:
            key.append(current_entity)
        triples = generate_knowledge_triples(current_entity)
        visited.add(current_entity)

        for triple in triples:
            all_triples.append(triple)
            next_entity = triple.get("t")
            relation = triple.get("r")

            # ✅ 只扩展知识概念类的“t”
            if relation in ALLOWED_RELATIONS and next_entity and next_entity not in visited:
                queue.append((next_entity, depth + 1))

    return all_triples, key

def build_knowledge_graph_from_keywords(keywords: list, output_dir: str = "kg_output", max_workers: int = 2):
    os.makedirs(output_dir, exist_ok=True)
    seen_triples = set()
    all_triples = []

    def process_keyword(seed):
        print(f"🌱 开始扩展知识图谱：{seed}")
        triples = generate_knowledge_triples(seed)
        return seed, triples

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_keyword, kw) for kw in keywords]
        for future in as_completed(futures):
            seed, graph = future.result()
            for triple in graph:
                triple_str = json.dumps(triple, ensure_ascii=False)
                if triple_str not in seen_triples:
                    seen_triples.add(triple_str)
                    all_triples.append(triple)

    # 写入到统一文件
    # output_path = os.path.join(output_dir, "kg_expanded.jsonl")
    # with open(output_path, "w", encoding="utf-8") as f:
    #     for triple in all_triples:
    #         f.write(json.dumps(triple, ensure_ascii=False) + "\n")
    #
    # print(f"\n✅ 所有图谱扩展完成，合计生成 {len(all_triples)} 条三元组")
    # print(f"📁 输出已统一保存至：{output_path}")
    return all_triples

# 运行入口
if __name__ == "__main__":
    sentence = "【准确率】：60%\n\n【反馈】：候选人回答了装甲板识别模块和模型融合策略的部分内容，但缺乏细节和准确性。装甲板识别模块的描述过于简略，未提及具体实现方法；人工智能算法精英赛部分仅提到融合策略，未涉及DEGCN、SkateFormer等模型的集成过程及提高识别精度的具体措施。\n\n【改进建议】：\n– 补充装甲板识别模块的具体实现步骤，如图像预处理、特征提取、目标检测流程等\n– 说明在集成DEGCN、SkateFormer时采用的技术细节（如模型结构调整、训练策略等）\n– 举例说明如何通过多模型融合提升识别精度（如对比单一模型与融合后的性能指标）\n– 明确\"Soft Voting\"策略中权重分配的具体依据（如验证集性能指标量化标准）"
    keywords = summary_word(sentence)
    print(keywords)
    output_dir = r"D:\AllFiles\competition\soft\Screening-LLM\data\graph"
    all_triplets = build_knowledge_graph_from_keywords(keywords)
    print(all_triplets)

    # seed = input("请输入知识起始词：").strip()
    # graph = build_knowledge_graph(seed, max_depth=2, max_nodes=50)
    #
    # # 保存
    # output_path = f"kg_{seed}_expanded.jsonl"
    # with open(output_path, "w", encoding="utf-8") as f:
    #     for triple in graph:
    #         f.write(json.dumps(triple, ensure_ascii=False) + "\n")
    #
    # print(f"\n✅ 知识图谱扩展完成，共生成 {len(graph)} 条三元组")
    # print(f"📁 输出已保存到：{output_path}")
