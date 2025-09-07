#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用正确PDF URL的详细信息爬虫
"""

import requests
import PyPDF2
import io
import json
import re
from datetime import datetime
from typing import List, Dict, Set

def extract_detailed_info_from_pdfs():
    """从正确的PDF文件中提取详细信息"""
    print("🎯 使用正确PDF URL提取详细信息")
    print("=" * 50)
    
    # 正确的PDF URL
    pdf_urls = [
        ("完整论文集", "https://meow.elettra.eu/82/pdf/hiat2025_proceedings_volume.pdf"),
        ("论文概览", "https://meow.elettra.eu/82/pdf/hiat2025_proceedings_brief.pdf")
    ]
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    results = {
        "conference_info": {
            "name": "HIAT2025",
            "full_name": "16th International Conference on Heavy Ion Accelerator Technology",
            "date": "22-27 June 2025",
            "location": "Michigan State University, East Lansing, USA",
            "host": "Facility for Rare Isotope Beams (FRIB)"
        },
        "extracted_authors": [],
        "extracted_institutions": [],
        "extracted_papers": [],
        "technical_keywords": [],
        "pdf_analysis": {}
    }
    
    for pdf_name, pdf_url in pdf_urls:
        print(f"\n📚 分析 {pdf_name}")
        print(f"URL: {pdf_url}")
        
        try:
            response = session.get(pdf_url, timeout=60)
            print(f"HTTP状态: {response.status_code}")
            print(f"文件大小: {len(response.content):,} 字节")
            
            if response.status_code == 200 and len(response.content) > 100000:  # 至少100KB
                pdf_file = io.BytesIO(response.content)
                reader = PyPDF2.PdfReader(pdf_file)
                
                total_pages = len(reader.pages)
                print(f"PDF页数: {total_pages}")
                
                # 分析策略：分析前20页获取作者和论文信息
                pages_to_analyze = min(20, total_pages)
                print(f"分析页数: {pages_to_analyze}")
                
                all_text = ""
                authors_found = set()
                institutions_found = set()
                papers_found = []
                
                for page_num in range(pages_to_analyze):
                    try:
                        page = reader.pages[page_num]
                        page_text = page.extract_text()
                        
                        if page_text and len(page_text.strip()) > 50:
                            all_text += page_text + "\n"
                            
                            # 从每页提取信息
                            page_authors = extract_authors_from_page(page_text)
                            page_institutions = extract_institutions_from_page(page_text)
                            page_papers = extract_papers_from_page(page_text)
                            
                            authors_found.update(page_authors)
                            institutions_found.update(page_institutions)
                            papers_found.extend(page_papers)
                            
                            if page_num < 5:  # 显示前5页的样本
                                print(f"   页面{page_num+1}: {len(page_text)} 字符")
                                
                    except Exception as e:
                        print(f"   页面{page_num+1}处理失败: {str(e)}")
                        continue
                
                # 汇总分析结果
                pdf_analysis = {
                    "name": pdf_name,
                    "url": pdf_url,
                    "total_pages": total_pages,
                    "analyzed_pages": pages_to_analyze,
                    "total_text_length": len(all_text),
                    "authors_count": len(authors_found),
                    "institutions_count": len(institutions_found),
                    "papers_count": len(papers_found)
                }
                
                results["pdf_analysis"][pdf_name] = pdf_analysis
                results["extracted_authors"].extend(list(authors_found))
                results["extracted_institutions"].extend(list(institutions_found))
                results["extracted_papers"].extend(papers_found)
                
                print(f"✅ {pdf_name}分析完成:")
                print(f"   作者: {len(authors_found)}")
                print(f"   机构: {len(institutions_found)}")
                print(f"   论文: {len(papers_found)}")
                
                # 保存文本样本
                if all_text.strip():
                    sample_file = f"pdf_content_{pdf_name.replace(' ', '_')}.txt"
                    with open(sample_file, 'w', encoding='utf-8') as f:
                        f.write(f"PDF: {pdf_name}\nURL: {pdf_url}\n\n")
                        f.write(all_text[:5000])  # 保存前5000字符
                    print(f"   文本样本已保存: {sample_file}")
                
            else:
                print(f"❌ PDF访问失败: 状态{response.status_code}, 大小{len(response.content)}")
                
        except Exception as e:
            print(f"❌ PDF处理失败: {str(e)}")
            continue
    
    # 去重和清理
    unique_authors = list(set(results["extracted_authors"]))
    unique_institutions = list(set(results["extracted_institutions"]))
    
    # 过滤和验证
    verified_authors = [author for author in unique_authors if is_valid_author_name(author)]
    verified_institutions = [inst for inst in unique_institutions if is_valid_institution_name(inst)]
    
    results["verified_authors"] = verified_authors
    results["verified_institutions"] = verified_institutions
    
    # 提取技术关键词
    physics_keywords = [
        'accelerator', 'beam', 'ion', 'heavy ion', 'proton', 'electron',
        'synchrotron', 'cyclotron', 'linac', 'radiofrequency', 'rf',
        'superconducting', 'magnet', 'cavity', 'injection', 'extraction',
        'collider', 'isotope', 'radioisotope', 'neutron', 'target'
    ]
    
    found_keywords = []
    all_content = ' '.join([results["pdf_analysis"].get(pdf, {}).get("name", "") for pdf in results["pdf_analysis"]])
    
    for keyword in physics_keywords:
        if keyword in all_content.lower():
            found_keywords.append(keyword)
    
    results["technical_keywords"] = found_keywords
    
    # 生成统计
    results["statistics"] = {
        "total_verified_authors": len(verified_authors),
        "total_verified_institutions": len(verified_institutions),
        "total_technical_keywords": len(found_keywords),
        "total_papers": len(results["extracted_papers"]),
        "pdf_files_processed": len(results["pdf_analysis"]),
        "extraction_timestamp": datetime.now().isoformat()
    }
    
    return results

def extract_authors_from_page(text: str) -> Set[str]:
    """从页面文本中提取作者"""
    authors = set()
    
    # 作者姓名模式
    patterns = [
        r'\b([A-Z][a-z]{2,15}\s+[A-Z][a-z]{2,15})\b',  # John Smith
        r'\b([A-Z][a-z]{2,15}\s+[A-Z]\.\s+[A-Z][a-z]{2,15})\b',  # John A. Smith
        r'\b([A-Z]\.\s*[A-Z][a-z]{2,15})\b',  # A. Smith
        r'\b([A-Z][a-z]{2,15},\s*[A-Z][a-z]{2,15})\b'  # Smith, John
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if is_valid_author_name(match):
                authors.add(match.strip())
    
    return authors

def extract_institutions_from_page(text: str) -> Set[str]:
    """从页面文本中提取机构"""
    institutions = set()
    
    patterns = [
        r'\b([A-Z][a-zA-Z\s]{5,40}\s+University)\b',
        r'\b(University\s+of\s+[A-Z][a-zA-Z\s]{3,30})\b',
        r'\b([A-Z][a-zA-Z\s]{5,40}\s+Institute)\b',
        r'\b([A-Z][a-zA-Z\s]{5,40}\s+Laboratory)\b',
        r'\b(Michigan State University)\b',
        r'\b(FRIB|NSCL|CERN|DESY|KEK|SLAC|Fermilab)\b'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if is_valid_institution_name(match):
                institutions.add(match.strip())
    
    return institutions

def extract_papers_from_page(text: str) -> List[Dict]:
    """从页面文本中提取论文标题"""
    papers = []
    
    # 查找论文标题（通常是较长的大写或标题格式文本）
    title_patterns = [
        r'\n([A-Z][A-Z\s\-:]{20,100})\n',
        r'\n([A-Z][a-zA-Z\s\-:]{25,120})\n'
    ]
    
    for pattern in title_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            title = match.strip()
            if is_valid_paper_title(title):
                papers.append({
                    "title": title,
                    "source": "pdf_extraction"
                })
    
    return papers

def is_valid_author_name(name: str) -> bool:
    """验证作者姓名"""
    if not name or len(name) < 4 or len(name) > 50:
        return False
    
    # 排除明显不是姓名的词
    invalid_words = [
        'Abstract', 'Conference', 'Proceedings', 'Volume', 'Session',
        'Committee', 'Program', 'Schedule', 'Heavy Ion', 'Accelerator',
        'Technology', 'Physics', 'Publishing', 'Creative Commons'
    ]
    
    for invalid in invalid_words:
        if invalid.lower() in name.lower():
            return False
    
    # 检查姓名结构
    parts = name.split()
    if len(parts) < 2:
        return False
    
    # 每个部分应该以大写字母开头
    for part in parts:
        if not part[0].isupper():
            return False
    
    return True

def is_valid_institution_name(name: str) -> bool:
    """验证机构名称"""
    if not name or len(name) < 5 or len(name) > 100:
        return False
    
    institution_keywords = [
        'University', 'Institute', 'Laboratory', 'Lab', 'Center',
        'College', 'School', 'FRIB', 'NSCL', 'CERN', 'DESY'
    ]
    
    return any(keyword in name for keyword in institution_keywords)

def is_valid_paper_title(title: str) -> bool:
    """验证论文标题"""
    if not title or len(title) < 15 or len(title) > 200:
        return False
    
    invalid_indicators = [
        'Page', 'Table', 'Figure', 'Abstract', 'Session',
        'Track', 'Program', 'Schedule', 'Proceedings'
    ]
    
    return not any(indicator in title for indicator in invalid_indicators)

def main():
    """主函数"""
    print("🚀 HIAT2025 PDF详细信息提取器")
    print("使用正确的PDF URL获取作者、机构和论文信息")
    print()
    
    try:
        results = extract_detailed_info_from_pdfs()
        
        # 保存结果
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = f"hiat2025_pdf_extraction_{timestamp}.json"
        
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # 显示总结
        stats = results["statistics"]
        print(f"\n🎉 PDF信息提取完成！")
        print("=" * 40)
        print(f"📊 验证作者: {stats['total_verified_authors']} 位")
        print(f"🏛️ 验证机构: {stats['total_verified_institutions']} 个")
        print(f"🔬 技术关键词: {stats['total_technical_keywords']} 个")
        print(f"📄 论文标题: {stats['total_papers']} 篇")
        print(f"📚 处理PDF: {stats['pdf_files_processed']} 个")
        print()
        print(f"💾 完整结果已保存: {result_file}")
        
        if stats['total_verified_authors'] > 0:
            print("\n👥 验证作者示例 (前10位):")
            for i, author in enumerate(results["verified_authors"][:10], 1):
                print(f"   {i}. {author}")
        
        if stats['total_verified_institutions'] > 0:
            print("\n🏛️ 验证机构示例 (前5个):")
            for i, inst in enumerate(results["verified_institutions"][:5], 1):
                print(f"   {i}. {inst}")
        
        print(f"\n🌟 成功从PDF文档中提取了详细的会议信息！")
        
    except Exception as e:
        print(f"❌ 程序执行失败: {str(e)}")
        print("💡 建议检查网络连接和PyPDF2安装")

if __name__ == "__main__":
    main()
