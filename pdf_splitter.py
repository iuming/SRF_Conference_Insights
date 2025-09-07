#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF论文分割器
将会议论文集PDF按照单篇论文分割成独立的PDF文件
"""

import PyPDF2
import os
import re
import json
from datetime import datetime
from typing import List, Dict, Tuple
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PDFPaperSplitter:
    """PDF论文分割器"""
    
    def __init__(self, output_dir: str = "individual_papers"):
        self.output_dir = output_dir
        self.split_results = {
            "split_papers": [],
            "total_papers": 0,
            "total_pages": 0,
            "split_info": {},
            "failed_splits": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # 创建输出目录
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logger.info(f"创建输出目录: {self.output_dir}")
    
    def split_conference_proceedings(self, pdf_path: str) -> Dict:
        """分割会议论文集"""
        logger.info(f"🔪 开始分割PDF: {pdf_path}")
        
        if not os.path.exists(pdf_path):
            logger.error(f"PDF文件不存在: {pdf_path}")
            return self.split_results
        
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                total_pages = len(reader.pages)
                
                logger.info(f"📖 PDF总页数: {total_pages}")
                
                # 分析论文边界
                paper_boundaries = self._detect_paper_boundaries(reader)
                logger.info(f"🔍 检测到 {len(paper_boundaries)} 个论文边界")
                
                # 分割每篇论文
                for i, (start_page, end_page, title) in enumerate(paper_boundaries):
                    try:
                        self._extract_single_paper(reader, start_page, end_page, title, i + 1)
                    except Exception as e:
                        logger.error(f"分割第{i+1}篇论文失败: {str(e)}")
                        self.split_results["failed_splits"].append({
                            "paper_number": i + 1,
                            "start_page": start_page,
                            "end_page": end_page,
                            "title": title,
                            "error": str(e)
                        })
                
                self.split_results["total_papers"] = len(paper_boundaries)
                self.split_results["total_pages"] = total_pages
                
        except Exception as e:
            logger.error(f"PDF处理失败: {str(e)}")
            
        return self.split_results
    
    def _detect_paper_boundaries(self, reader: PyPDF2.PdfReader) -> List[Tuple[int, int, str]]:
        """检测论文边界"""
        logger.info("🔍 正在检测论文边界...")
        
        boundaries = []
        current_paper_start = 0
        
        # 论文标题的常见模式
        title_patterns = [
            r'^[A-Z][A-Z\s]{10,80}$',  # 全大写标题
            r'^[A-Z][a-zA-Z\s\-:]{15,100}$',  # 标准标题格式
            r'^\w+\d+\s*[-–]\s*[A-Z][a-zA-Z\s\-:]{10,80}$',  # 带编号的标题 (如 MOX01 - TITLE)
        ]
        
        # 论文结束的标识
        end_indicators = [
            'REFERENCES',
            'CONCLUSION',
            'ACKNOWLEDGMENTS',
            'ACKNOWLEDGEMENTS'
        ]
        
        total_pages = len(reader.pages)
        
        for page_num in range(total_pages):
            try:
                page = reader.pages[page_num]
                text = page.extract_text()
                
                if not text:
                    continue
                
                lines = text.split('\n')
                clean_lines = [line.strip() for line in lines if line.strip()]
                
                # 查找论文标题
                for line in clean_lines[:10]:  # 只检查前10行
                    if self._is_paper_title(line, title_patterns):
                        # 如果找到新标题，保存前一篇论文
                        if page_num > current_paper_start:
                            prev_title = self._extract_title_from_page(reader, current_paper_start)
                            boundaries.append((current_paper_start, page_num - 1, prev_title))
                        
                        current_paper_start = page_num
                        break
        
        # 添加最后一篇论文
        if current_paper_start < total_pages - 1:
            last_title = self._extract_title_from_page(reader, current_paper_start)
            boundaries.append((current_paper_start, total_pages - 1, last_title))
        
        # 如果没有检测到明确的边界，使用智能分割
        if len(boundaries) < 5:  # 论文数量太少，可能检测有问题
            logger.warning("检测到的论文数量较少，使用智能分割模式...")
            boundaries = self._intelligent_split(reader)
        
        return boundaries
    
    def _is_paper_title(self, line: str, patterns: List[str]) -> bool:
        """判断是否为论文标题"""
        if len(line) < 10 or len(line) > 100:
            return False
        
        # 排除明显不是标题的行
        exclude_keywords = {
            'page', 'proceedings', 'conference', 'abstract', 'figure', 'table',
            'introduction', 'conclusion', 'references', 'acknowledgment',
            'copyright', 'isbn', 'doi', 'email', 'university', 'laboratory'
        }
        
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in exclude_keywords):
            return False
        
        # 检查是否匹配标题模式
        for pattern in patterns:
            if re.match(pattern, line):
                return True
        
        # 检查是否包含论文编号模式 (如 MOX01, TUP11等)
        if re.match(r'^[A-Z]{2,3}\d{2}\s*[-–]\s*', line):
            return True
        
        return False
    
    def _extract_title_from_page(self, reader: PyPDF2.PdfReader, page_num: int) -> str:
        """从页面提取标题"""
        try:
            page = reader.pages[page_num]
            text = page.extract_text()
            
            if not text:
                return f"Paper_{page_num + 1}"
            
            lines = text.split('\n')
            clean_lines = [line.strip() for line in lines if line.strip()]
            
            # 查找最可能的标题
            for line in clean_lines[:15]:  # 检查前15行
                if 10 <= len(line) <= 100:
                    # 清理标题
                    clean_title = self._clean_title(line)
                    if clean_title:
                        return clean_title
            
            # 如果没找到合适的标题，使用页码
            return f"Paper_Page_{page_num + 1}"
            
        except Exception as e:
            logger.warning(f"提取第{page_num + 1}页标题失败: {str(e)}")
            return f"Paper_{page_num + 1}"
    
    def _clean_title(self, title: str) -> str:
        """清理标题"""
        # 移除特殊字符和多余空格
        title = re.sub(r'[^\w\s\-]', '', title)
        title = re.sub(r'\s+', ' ', title)
        title = title.strip()
        
        # 限制长度
        if len(title) > 60:
            title = title[:60]
        
        # 移除不合适的字符作为文件名
        title = re.sub(r'[<>:"/\\|?*]', '_', title)
        
        return title
    
    def _intelligent_split(self, reader: PyPDF2.PdfReader) -> List[Tuple[int, int, str]]:
        """智能分割模式"""
        logger.info("🤖 使用智能分割模式...")
        
        total_pages = len(reader.pages)
        boundaries = []
        
        # 方法1: 基于内容变化检测
        content_changes = []
        
        for page_num in range(1, total_pages):
            try:
                prev_page = reader.pages[page_num - 1]
                curr_page = reader.pages[page_num]
                
                prev_text = prev_page.extract_text()
                curr_text = curr_page.extract_text()
                
                # 检测内容大幅变化
                if self._detect_content_break(prev_text, curr_text):
                    content_changes.append(page_num)
                    
            except Exception as e:
                continue
        
        # 方法2: 基于页面数估算
        if len(content_changes) < 10:  # 如果检测到的分割点太少
            # 假设平均每篇论文4-8页
            estimated_papers = total_pages // 6
            if estimated_papers > 0:
                pages_per_paper = total_pages // estimated_papers
                content_changes = list(range(0, total_pages, pages_per_paper))
        
        # 生成边界
        for i, start_page in enumerate(content_changes):
            end_page = content_changes[i + 1] - 1 if i + 1 < len(content_changes) else total_pages - 1
            title = self._extract_title_from_page(reader, start_page)
            boundaries.append((start_page, end_page, title))
        
        logger.info(f"智能分割检测到 {len(boundaries)} 篇论文")
        return boundaries
    
    def _detect_content_break(self, prev_text: str, curr_text: str) -> bool:
        """检测内容断点"""
        if not prev_text or not curr_text:
            return False
        
        # 检测参考文献结束
        if 'REFERENCES' in prev_text.upper() and 'REFERENCES' not in curr_text.upper():
            return True
        
        # 检测新标题开始（大写字母开头的长行）
        curr_lines = curr_text.split('\n')
        for line in curr_lines[:5]:
            line = line.strip()
            if len(line) > 15 and line[0].isupper() and line.upper() == line:
                return True
        
        # 检测论文编号模式
        if re.search(r'^[A-Z]{2,3}\d{2}\s*[-–]', curr_text[:100]):
            return True
        
        return False
    
    def _extract_single_paper(self, reader: PyPDF2.PdfReader, start_page: int, end_page: int, title: str, paper_number: int):
        """提取单篇论文"""
        logger.info(f"📄 提取第{paper_number}篇论文: {title} (页面 {start_page + 1}-{end_page + 1})")
        
        # 创建安全的文件名
        safe_title = self._make_safe_filename(title)
        filename = f"{paper_number:03d}_{safe_title}.pdf"
        output_path = os.path.join(self.output_dir, filename)
        
        try:
            writer = PyPDF2.PdfWriter()
            
            # 添加页面到新PDF
            for page_num in range(start_page, end_page + 1):
                if page_num < len(reader.pages):
                    writer.add_page(reader.pages[page_num])
            
            # 保存PDF文件
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            # 记录成功信息
            file_size = os.path.getsize(output_path)
            paper_info = {
                "paper_number": paper_number,
                "title": title,
                "filename": filename,
                "output_path": output_path,
                "start_page": start_page + 1,  # 显示时从1开始
                "end_page": end_page + 1,
                "total_pages": end_page - start_page + 1,
                "file_size_kb": round(file_size / 1024, 2),
                "status": "success"
            }
            
            self.split_results["split_papers"].append(paper_info)
            logger.info(f"   ✅ 保存成功: {filename} ({paper_info['total_pages']}页, {paper_info['file_size_kb']}KB)")
            
        except Exception as e:
            logger.error(f"   ❌ 保存失败: {str(e)}")
            raise
    
    def _make_safe_filename(self, title: str) -> str:
        """创建安全的文件名"""
        # 移除或替换不安全的字符
        safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
        safe_title = re.sub(r'\s+', '_', safe_title)
        safe_title = safe_title.strip('_')
        
        # 限制长度
        if len(safe_title) > 50:
            safe_title = safe_title[:50]
        
        # 确保不为空
        if not safe_title:
            safe_title = "Untitled_Paper"
        
        return safe_title
    
    def save_split_report(self) -> str:
        """保存分割报告"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"pdf_split_report_{timestamp}.json"
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(self.split_results, f, ensure_ascii=False, indent=2)
            
            logger.info(f"📊 分割报告已保存: {report_file}")
            
            # 生成文本报告
            txt_report = f"pdf_split_summary_{timestamp}.txt"
            self._generate_text_summary(txt_report)
            
            return report_file
            
        except Exception as e:
            logger.error(f"保存报告失败: {str(e)}")
            return ""
    
    def _generate_text_summary(self, filename: str):
        """生成文本摘要"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("PDF论文分割摘要报告\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"分割时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"总论文数: {self.split_results['total_papers']}\n")
            f.write(f"成功分割: {len(self.split_results['split_papers'])}\n")
            f.write(f"失败数量: {len(self.split_results['failed_splits'])}\n")
            f.write(f"输出目录: {self.output_dir}\n\n")
            
            f.write("分割详情:\n")
            f.write("-" * 30 + "\n")
            
            for paper in self.split_results['split_papers']:
                f.write(f"{paper['paper_number']:3d}. {paper['title']}\n")
                f.write(f"     文件: {paper['filename']}\n")
                f.write(f"     页面: {paper['start_page']}-{paper['end_page']} ({paper['total_pages']}页)\n")
                f.write(f"     大小: {paper['file_size_kb']}KB\n\n")
            
            if self.split_results['failed_splits']:
                f.write("\n失败的分割:\n")
                f.write("-" * 20 + "\n")
                for failed in self.split_results['failed_splits']:
                    f.write(f"论文 {failed['paper_number']}: {failed['title']}\n")
                    f.write(f"错误: {failed['error']}\n\n")
        
        logger.info(f"📋 文本摘要已生成: {filename}")

def main():
    """主函数"""
    print("🔪 HIAT2025 PDF论文分割器")
    print("=" * 60)
    print()
    print("🚀 功能:")
    print("✅ 自动检测论文边界")
    print("✅ 按论文分割PDF")
    print("✅ 智能标题识别")
    print("✅ 生成分割报告")
    print()
    
    # 检查PDF文件
    pdf_files = [
        "downloaded_pdfs/hiat2025_proceedings_volume.pdf",
        "downloaded_pdfs/hiat2025_proceedings_brief.pdf"
    ]
    
    available_files = [f for f in pdf_files if os.path.exists(f)]
    
    if not available_files:
        print("❌ 未找到PDF文件，请先运行 pdf_downloader_analyzer.py 下载PDF")
        return
    
    print("📂 找到PDF文件:")
    for i, pdf_file in enumerate(available_files, 1):
        file_size_mb = os.path.getsize(pdf_file) / (1024 * 1024)
        print(f"  {i}. {pdf_file} ({file_size_mb:.1f} MB)")
    
    print("\n🔍 选择要分割的PDF文件:")
    print("1. 完整论文集 (推荐 - 包含完整论文)")
    print("2. 论文概览 (较短版本)")
    print("3. 分割所有文件")
    
    try:
        choice = input("\n请选择 (1/2/3): ").strip()
        
        splitter = PDFPaperSplitter()
        
        if choice == "1":
            if "volume.pdf" in str(available_files):
                pdf_path = next(f for f in available_files if "volume.pdf" in f)
                print(f"\n🔪 分割文件: {pdf_path}")
                splitter.split_conference_proceedings(pdf_path)
            else:
                print("❌ 完整论文集文件未找到")
                return
                
        elif choice == "2":
            if "brief.pdf" in str(available_files):
                pdf_path = next(f for f in available_files if "brief.pdf" in f)
                print(f"\n🔪 分割文件: {pdf_path}")
                splitter.split_conference_proceedings(pdf_path)
            else:
                print("❌ 论文概览文件未找到")
                return
                
        elif choice == "3":
            for pdf_path in available_files:
                print(f"\n🔪 分割文件: {pdf_path}")
                splitter.split_conference_proceedings(pdf_path)
        else:
            print("❌ 无效选择")
            return
        
        # 保存报告
        print("\n💾 保存分割报告...")
        report_file = splitter.save_split_report()
        
        # 显示结果
        results = splitter.split_results
        print("\n" + "=" * 60)
        print("🎉 PDF分割完成！")
        print("=" * 60)
        print(f"📊 总论文数: {results['total_papers']}")
        print(f"✅ 成功分割: {len(results['split_papers'])}")
        print(f"❌ 失败数量: {len(results['failed_splits'])}")
        print(f"📁 输出目录: {splitter.output_dir}")
        
        if results['split_papers']:
            total_size_kb = sum(p['file_size_kb'] for p in results['split_papers'])
            print(f"📄 总文件大小: {total_size_kb/1024:.1f} MB")
            
            print(f"\n📋 分割的论文 (前10篇):")
            for paper in results['split_papers'][:10]:
                print(f"  {paper['paper_number']:3d}. {paper['filename']} ({paper['total_pages']}页)")
            
            if len(results['split_papers']) > 10:
                print(f"  ... 还有 {len(results['split_papers']) - 10} 篇论文")
        
        print(f"\n🌟 分割完成！您现在可以:")
        print(f"  1. 打开 {splitter.output_dir} 目录查看分割的PDF文件")
        print(f"  2. 单独阅读每篇论文")
        print(f"  3. 查看分割报告了解详情")
        print(f"  4. 根据需要重新组织文件")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ 用户取消操作")
    except Exception as e:
        print(f"\n❌ 程序执行失败: {str(e)}")
        print("💡 建议:")
        print("  1. 检查PDF文件是否存在且可读")
        print("  2. 确保有足够的磁盘空间")
        print("  3. 确保有写入权限")

if __name__ == "__main__":
    main()
