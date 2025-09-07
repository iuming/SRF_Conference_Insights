#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据处理脚本 - 为GitHub Pages准备数据
将提取的PDF内容转换为前端可用的JSON格式
"""

import json
import os
import sys
import shutil
from pathlib import Path
import base64
from datetime import datetime

class DataProcessor:
    """数据处理器 - 为前端准备数据"""
    
    def __init__(self, source_dir=".", output_dir="docs"):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.data_dir = self.output_dir / "data"
        self.images_dir = self.output_dir / "images"
        
        # 创建输出目录
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(parents=True, exist_ok=True)
    
    def process_all_data(self):
        """处理所有数据"""
        print("🔄 开始处理数据...")
        
        # 1. 查找并处理JSON数据文件
        json_files = list(self.source_dir.glob("content_extraction_full_*.json"))
        if not json_files:
            print("❌ 未找到内容提取的JSON文件")
            return False
        
        latest_json = max(json_files, key=os.path.getctime)
        print(f"📄 使用数据文件: {latest_json}")
        
        # 2. 加载和处理论文数据
        with open(latest_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        papers_data = self.process_papers_data(data)
        
        # 3. 保存处理后的数据
        self.save_papers_data(papers_data)
        
        # 4. 处理图片
        self.process_images()
        
        # 5. 生成统计数据
        self.generate_statistics(papers_data)
        
        # 6. 复制必要的文件
        self.copy_static_files()
        
        print("✅ 数据处理完成!")
        return True
    
    def process_papers_data(self, data):
        """处理论文数据"""
        papers = data.get('papers', [])
        processed_papers = []
        
        print(f"📚 处理 {len(papers)} 篇论文...")
        
        for paper in papers:
            processed_paper = {
                'paper_number': paper.get('paper_number', 0),
                'filename': paper.get('filename', ''),
                'title': paper.get('title', ''),
                'authors': paper.get('authors', []),
                'affiliations': paper.get('affiliations', []),
                'abstract': paper.get('abstract', ''),
                'keywords': paper.get('keywords', []),
                'page_count': paper.get('page_count', 0),
                'file_size_kb': paper.get('file_size_kb', 0),
                'figures': paper.get('figures', []),
                'tables': paper.get('tables', []),
                'references': paper.get('references', []),
                'sections': paper.get('sections', {}),
                'reference_count': len(paper.get('references', [])),
                'figure_count': len(paper.get('figures', [])),
                'table_count': len(paper.get('tables', []))
            }
            processed_papers.append(processed_paper)
        
        return {
            'extraction_time': data.get('extraction_time', ''),
            'total_papers': len(processed_papers),
            'papers': processed_papers
        }
    
    def save_papers_data(self, papers_data):
        """保存论文数据"""
        output_file = self.data_dir / "papers.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(papers_data, f, ensure_ascii=False, indent=2)
        print(f"💾 论文数据已保存: {output_file}")
    
    def process_images(self):
        """处理图片文件"""
        source_images_dir = self.source_dir / "extracted_content" / "images"
        if not source_images_dir.exists():
            print("⚠️ 未找到图片目录")
            return
        
        print("🖼️ 处理图片文件...")
        
        # 复制前100张图片作为示例
        image_files = list(source_images_dir.glob("*.png"))[:100]
        
        for i, img_file in enumerate(image_files):
            dest_file = self.images_dir / img_file.name
            try:
                shutil.copy2(img_file, dest_file)
                if i % 20 == 0:
                    print(f"  📸 已复制 {i+1}/{len(image_files)} 张图片")
            except Exception as e:
                print(f"❌ 复制图片失败 {img_file}: {e}")
        
        print(f"✅ 已复制 {len(image_files)} 张图片")
    
    def generate_statistics(self, papers_data):
        """生成统计数据"""
        papers = papers_data['papers']
        
        # 基本统计
        stats = {
            'total_papers': len(papers),
            'total_pages': sum(p['page_count'] for p in papers),
            'total_authors': len(set(author for p in papers for author in p['authors'])),
            'total_institutions': len(set(aff for p in papers for aff in p['affiliations'])),
            'total_figures': sum(p['figure_count'] for p in papers),
            'total_tables': sum(p['table_count'] for p in papers),
            'total_references': sum(p['reference_count'] for p in papers),
            'papers_with_abstract': sum(1 for p in papers if p['abstract']),
            'papers_with_keywords': sum(1 for p in papers if p['keywords']),
            'avg_pages': sum(p['page_count'] for p in papers) / len(papers) if papers else 0,
            'avg_figures': sum(p['figure_count'] for p in papers) / len(papers) if papers else 0,
            'avg_references': sum(p['reference_count'] for p in papers) / len(papers) if papers else 0
        }
        
        # 机构统计
        institution_counts = {}
        for paper in papers:
            for aff in paper['affiliations']:
                # 简化机构名称
                simple_name = aff.split(',')[0].strip()
                institution_counts[simple_name] = institution_counts.get(simple_name, 0) + 1
        
        top_institutions = sorted(institution_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # 关键词统计
        keyword_counts = {}
        for paper in papers:
            for keyword in paper['keywords']:
                keyword_counts[keyword.lower()] = keyword_counts.get(keyword.lower(), 0) + 1
        
        top_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:20]
        
        # 页数分布
        page_distribution = {'1-2页': 0, '3-4页': 0, '5-6页': 0, '7-8页': 0, '8+页': 0}
        for paper in papers:
            pages = paper['page_count']
            if pages <= 2: page_distribution['1-2页'] += 1
            elif pages <= 4: page_distribution['3-4页'] += 1
            elif pages <= 6: page_distribution['5-6页'] += 1
            elif pages <= 8: page_distribution['7-8页'] += 1
            else: page_distribution['8+页'] += 1
        
        # 图片分布
        figure_distribution = {'0-5图': 0, '6-10图': 0, '11-15图': 0, '16-20图': 0, '20+图': 0}
        for paper in papers:
            figures = paper['figure_count']
            if figures <= 5: figure_distribution['0-5图'] += 1
            elif figures <= 10: figure_distribution['6-10图'] += 1
            elif figures <= 15: figure_distribution['11-15图'] += 1
            elif figures <= 20: figure_distribution['16-20图'] += 1
            else: figure_distribution['20+图'] += 1
        
        complete_stats = {
            'basic_stats': stats,
            'top_institutions': top_institutions,
            'top_keywords': top_keywords,
            'page_distribution': page_distribution,
            'figure_distribution': figure_distribution,
            'generated_at': datetime.now().isoformat()
        }
        
        # 保存统计数据
        stats_file = self.data_dir / "statistics.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(complete_stats, f, ensure_ascii=False, indent=2)
        
        print(f"📊 统计数据已保存: {stats_file}")
    
    def copy_static_files(self):
        """复制必要的静态文件"""
        # 创建README文件
        readme_content = f"""# HIAT2025 论文内容分析系统

这是一个基于GitHub Pages的论文内容分析和查询系统。

## 数据更新时间
{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}

## 功能特性
- 📚 86篇论文的详细内容分析
- 🔍 智能搜索和过滤
- 📊 数据可视化图表
- 🖼️ 图片画廊浏览
- 📱 响应式设计

## 技术栈
- 前端: HTML5, CSS3, JavaScript, Bootstrap 5
- 图表: Chart.js
- 部署: GitHub Pages
- 数据处理: Python

## 访问地址
https://{os.environ.get('GITHUB_REPOSITORY_OWNER', 'username')}.github.io/{os.environ.get('GITHUB_REPOSITORY', 'repo').split('/')[-1]}/

## 数据来源
数据来源于HIAT2025重离子加速器技术国际会议论文集的深度分析。
"""
        
        readme_file = self.output_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"📄 README已生成: {readme_file}")

def main():
    """主函数"""
    print("🚀 HIAT2025 数据处理器")
    print("=" * 50)
    
    processor = DataProcessor()
    
    if processor.process_all_data():
        print("\n🎉 数据处理成功完成!")
        print("📂 输出目录结构:")
        print("  docs/")
        print("  ├── index.html        # 主页面")
        print("  ├── app.js           # 前端逻辑")
        print("  ├── data/")
        print("  │   ├── papers.json  # 论文数据")
        print("  │   └── statistics.json # 统计数据")
        print("  └── images/          # 图片文件")
        print("\n🌐 准备部署到GitHub Pages!")
    else:
        print("\n❌ 数据处理失败!")
        sys.exit(1)

if __name__ == "__main__":
    main()
