#!/usr/bin/env python3
"""
整合HIAT2025和IPAC2025的论文数据
"""

import json
import os
from datetime import datetime

def load_hiat_papers():
    """加载HIAT2025论文数据"""
    hiat_path = "../../conferences/HIAT2025/papers.json"
    try:
        with open(hiat_path, 'r', encoding='utf-8') as f:
            hiat_data = json.load(f)
            return hiat_data.get('papers', [])
    except Exception as e:
        print(f"无法加载HIAT2025数据: {e}")
        return []

def load_ipac_papers():
    """加载IPAC2025论文数据"""
    ipac_path = "ipac2025_papers.json"
    try:
        with open(ipac_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"无法加载IPAC2025数据: {e}")
        return []

def convert_hiat_format(hiat_papers):
    """转换HIAT论文格式为统一格式"""
    converted_papers = []
    
    for paper in hiat_papers:
        converted_paper = {
            "contribution_id": f"HIAT25_{paper.get('paper_number', 0):04d}",
            "paper_code": f"HIAT25-{paper.get('paper_number', 0):03d}",
            "title": paper.get('title', 'Unknown Title'),
            "authors": paper.get('authors', []),
            "institutions": paper.get('affiliations', [])[:3],  # 取前3个机构
            "abstract": paper.get('abstract', '')[:200] + "..." if paper.get('abstract') else "No abstract available",
            "keywords": [],  # HIAT数据中没有关键词
            "category": "Heavy Ion Accelerator Technology",
            "type": "Conference Paper",
            "datetime": "2025/6/22 9:00",  # HIAT2025时间
            "conference": "HIAT2025",
            "session": "HIAT",
            "pages": paper.get('page_count', 4),
            "doi": f"10.18429/JACoW-HIAT2025-{paper.get('paper_number', 0):03d}",
            "url": f"https://jacow.org/hiat2025/papers/{paper.get('filename', 'paper')}.pdf",
            "figures": len(paper.get('figures', [])),
            "tables": len(paper.get('tables', [])),
            "references": len(paper.get('references', [])),
            "file_size_kb": paper.get('file_size_kb', 0),
            "extraction_source": "HIAT2025"
        }
        converted_papers.append(converted_paper)
    
    return converted_papers

def convert_ipac_format(ipac_papers):
    """转换IPAC论文格式为统一格式"""
    for paper in ipac_papers:
        paper["extraction_source"] = "IPAC2025"
    return ipac_papers

def create_combined_dataset():
    """创建合并的数据集"""
    
    # 加载数据
    hiat_papers = load_hiat_papers()
    ipac_papers = load_ipac_papers()
    
    print(f"加载了 {len(hiat_papers)} 篇HIAT2025论文")
    print(f"加载了 {len(ipac_papers)} 篇IPAC2025论文")
    
    # 转换格式
    hiat_converted = convert_hiat_format(hiat_papers)
    ipac_converted = convert_ipac_format(ipac_papers)
    
    # 合并数据
    all_papers = hiat_converted + ipac_converted
    
    # 创建统计信息
    combined_data = {
        "extraction_time": datetime.now().isoformat(),
        "total_papers": len(all_papers),
        "conferences": {
            "HIAT2025": len(hiat_converted),
            "IPAC2025": len(ipac_converted)
        },
        "papers": all_papers
    }
    
    # 保存合并的数据
    with open("papers-combined.json", 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n合并完成！")
    print(f"总论文数: {len(all_papers)}")
    print(f"数据已保存到: papers-combined.json")
    
    return combined_data

if __name__ == "__main__":
    os.chdir("c:/Users/刘铭/Downloads/SRF_Conference_Insights/docs/data")
    combined_data = create_combined_dataset()
