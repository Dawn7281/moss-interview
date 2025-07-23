import json
import os
import re
import fitz  # PyMuPDF for PDF
import docx
from typing import Dict, List, Union


def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error reading PDF: {str(e)}")
        return ""


def extract_text_from_docx(docx_path: str) -> str:
    try:
        doc = docx.Document(docx_path)
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    except Exception as e:
        print(f"Error reading DOCX: {str(e)}")
        return ""


def clean_text(text: str) -> str:
    return re.sub(r"\n{2,}", "\n", text.strip())


def section_split(text: str) -> Dict[str, str]:
    """
    将简历文本按常见标题进行分段。
    返回格式：{ "教育经历": "...", "项目经历": "...", ... }
    """
    section_titles = [
        "基本信息", "个人信息", "教育经历","教育背景", "实习经历", "工作经历", "工作经验" , "项目经历", "项目经验",
        "技能", "技能特长","个人优势", "专业技能", "荣誉奖项", "奖项" , "荣誉证书", "证书", "自我评价", "个人总结"
    ]
    pattern = "|".join([fr"(?P<{t}>{t})" for t in section_titles])
    split_pattern = re.compile(rf"(?P<title>{pattern})", re.MULTILINE)

    sections = {}
    current_title = "其他"
    current_text = []

    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if any(title in line for title in section_titles):
            if current_text:
                sections[current_title] = "\n".join(current_text).strip()
                current_text = []
            current_title = next((t for t in section_titles if t in line), "其他")
        else:
            current_text.append(line)
    if current_text:
        sections[current_title] = "\n".join(current_text).strip()

    return sections


def parse_resume(resume_path: str) -> Dict[str, Union[str, List]]:
    ext = os.path.splitext(resume_path)[-1].lower()
    if ext == ".pdf":
        raw_text = extract_text_from_pdf(resume_path)
    elif ext in [".docx", ".doc"]:
        raw_text = extract_text_from_docx(resume_path)
    else:
        raise ValueError("Unsupported resume format. Only PDF and DOCX are supported.")

    text = clean_text(raw_text)
    sections = section_split(text)

    return {
        # "raw_text": text,
        # "sections": sections,
        "basic_info": sections.get("基本信息") or sections.get("个人信息", ""),
        "education": sections.get("教育经历", "") or sections.get("教育背景", ""),
        "experience": sections.get("实习经历", "") or sections.get("工作经历", "") or sections.get("工作经验", ""),
        "projects": sections.get("项目经历", "") or sections.get("项目经验", ""),
        "skills": sections.get("技能", "") or sections.get("专业技能", "") or sections.get("技能特长", "") or sections.get("个人优势", ""),
        "awards": sections.get("荣誉奖项", "") or sections.get("证书", "") or sections.get("奖项", "") or sections.get("荣誉证书", ""),
        "self_description": sections.get("自我评价", "") or sections.get("个人总结", "")
    }

def save_parsed_resume(result_dict, save_path="parsed_resume.json"):
    """
    保存解析后的简历内容到 JSON 文件中
    """
    try:
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(result_dict, f, ensure_ascii=False, indent=4)
        print(f"简历解析结果已保存至 {save_path}")
    except Exception as e:
        print(f"保存 JSON 文件失败: {str(e)}")

if __name__ == '__main__':
    resume_path = r"D:\AllFiles\competition\soft\Screening-LLM\data\cvs\杨璐雨简历-active.docx"
    result = parse_resume(resume_path)
    base_name = os.path.splitext(os.path.basename(resume_path))[0]
    save_path = rf"D:\AllFiles\competition\soft\Screening-LLM\data\json\{base_name}_parsed.json"
    save_parsed_resume(result, save_path)