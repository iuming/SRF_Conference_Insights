#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF论文分割器 - 简化版
将会议论文集PDF按照单篇论文分割成独立的PDF文件
"""

import PyPDF2
import os
import re
import json
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimplePDFSplitter:
    """简化版PDF分割器"""
    
    def __init__(self, output_dir="individual_papers"):
        self.output_dir = output_dir
        self.results = []
        
        # 创建输出目录
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logger.info(f"创建输出目录: {self.output_dir}")
    
    def split_by_pages(self, pdf_path, pages_per_paper=6):
        """按页数分割PDF"""
        logger.info(f"🔪 开始分割PDF: {pdf_path}")
        logger.info(f"📄 每篇论文预估页数: {pages_per_paper}")
        
        if not os.path.exists(pdf_path):
            logger.error(f"PDF文件不存在: {pdf_path}")
            return []
        
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                total_pages = len(reader.pages)
                
                logger.info(f"📖 PDF总页数: {total_pages}")
                
                paper_count = 0
                current_page = 0
                
                while current_page < total_pages:
                    paper_count += 1
                    
                    # 计算当前论文的页面范围
                    start_page = current_page
                    end_page = min(current_page + pages_per_paper - 1, total_pages - 1)
                    
                    # 提取标题
                    title = self.extract_title_from_page(reader, start_page)
                    
                    # 创建单篇论文PDF
                    success = self.create_paper_pdf(reader, start_page, end_page, title, paper_count)
                    
                    if success:
                        logger.info(f"✅ 第{paper_count}篇论文分割成功: 页面{start_page+1}-{end_page+1}")
                    
                    current_page = end_page + 1
                
                logger.info(f"🎉 分割完成！总共分割了 {paper_count} 篇论文")
                return self.results
                
        except Exception as e:
            logger.error(f"PDF处理失败: {str(e)}")
            return []
    
    def split_by_content(self, pdf_path):
        """按内容智能分割PDF"""
        logger.info(f"🤖 智能分割PDF: {pdf_path}")
        
        if not os.path.exists(pdf_path):
            logger.error(f"PDF文件不存在: {pdf_path}")
            return []
        
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                total_pages = len(reader.pages)
                
                logger.info(f"📖 PDF总页数: {total_pages}")
                
                # 检测分割点
                split_points = self.detect_paper_boundaries(reader)
                logger.info(f"🔍 检测到 {len(split_points)} 个分割点")
                
                # 按分割点创建论文
                for i, (start_page, end_page) in enumerate(split_points):
                    title = self.extract_title_from_page(reader, start_page)
                    success = self.create_paper_pdf(reader, start_page, end_page, title, i + 1)
                    
                    if success:
                        logger.info(f"✅ 第{i+1}篇论文分割成功: 页面{start_page+1}-{end_page+1}")
                
                logger.info(f"🎉 智能分割完成！总共分割了 {len(split_points)} 篇论文")
                return self.results
                
        except Exception as e:
            logger.error(f"智能分割失败: {str(e)}")
            return []
    
    def detect_paper_boundaries(self, reader):
        """检测论文边界"""
        total_pages = len(reader.pages)
        boundaries = []
        
        # 方法1: 寻找论文编号模式（如 MOX01, TUP11等）
        paper_starts = [0]  # 第一页总是开始
        
        for page_num in range(total_pages):
            try:
                page = reader.pages[page_num]
                text = page.extract_text()
                
                if text:
                    # 检查是否包含论文编号
                    if re.search(r'^[A-Z]{2,3}\d{2}\s*[-–]', text[:200]):
                        if page_num not in paper_starts:
                            paper_starts.append(page_num)
                    
                    # 检查是否包含新论文标题特征
                    lines = text.split('\n')[:10]
                    for line in lines:
                        line = line.strip()
                        if (len(line) > 20 and len(line) < 80 and 
                            line.isupper() and 'ABSTRACT' not in line and
                            'PROCEEDINGS' not in line):
                            if page_num not in paper_starts and page_num > 0:
                                paper_starts.append(page_num)
                            break
                            
            except Exception:
                continue
        
        # 如果检测的分割点太少，使用固定间隔
        if len(paper_starts) < 10:
            logger.warning("检测到的论文数量较少，使用固定间隔分割")
            estimated_papers = max(10, total_pages // 6)
            pages_per_paper = total_pages // estimated_papers
            paper_starts = list(range(0, total_pages, pages_per_paper))
        
        # 生成边界对
        paper_starts.sort()
        for i, start in enumerate(paper_starts):
            if i + 1 < len(paper_starts):
                end = paper_starts[i + 1] - 1
            else:
                end = total_pages - 1
            
            if start <= end:
                boundaries.append((start, end))
        
        return boundaries
    
    def extract_title_from_page(self, reader, page_num):
        """从页面提取标题"""
        try:
            page = reader.pages[page_num]
            text = page.extract_text()
            
            if not text:
                return f"Paper_{page_num + 1}"
            
            lines = text.split('\n')
            
            # 查找合适的标题
            for line in lines[:20]:
                line = line.strip()
                if 10 <= len(line) <= 80:
                    # 清理标题作为文件名
                    clean_title = re.sub(r'[^\w\s\-]', '', line)
                    clean_title = re.sub(r'\s+', '_', clean_title)
                    if clean_title and len(clean_title) > 5:
                        return clean_title[:50]  # 限制长度
            
            return f"Paper_Page_{page_num + 1}"
            
        except Exception:
            return f"Paper_{page_num + 1}"
    
    def create_paper_pdf(self, reader, start_page, end_page, title, paper_number):
        """创建单篇论文PDF"""
        try:
            # 创建安全的文件名
            safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
            filename = f"{paper_number:03d}_{safe_title}.pdf"
            output_path = os.path.join(self.output_dir, filename)
            
            # 创建新的PDF写入器
            writer = PyPDF2.PdfWriter()
            
            # 添加页面
            for page_num in range(start_page, end_page + 1):
                if page_num < len(reader.pages):
                    writer.add_page(reader.pages[page_num])
            
            # 保存文件
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            # 记录结果
            file_size = os.path.getsize(output_path)
            result = {
                "paper_number": paper_number,
                "title": title,
                "filename": filename,
                "output_path": output_path,
                "start_page": start_page + 1,
                "end_page": end_page + 1,
                "total_pages": end_page - start_page + 1,
                "file_size_kb": round(file_size / 1024, 2),
                "status": "success"
            }
            
            self.results.append(result)
            return True
            
        except Exception as e:
            logger.error(f"创建论文PDF失败: {str(e)}")
            return False
    
    def save_report(self):
        """保存分割报告"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON报告
        json_file = f"split_report_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        # 文本报告
        txt_file = f"split_summary_{timestamp}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write("PDF分割报告\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"分割时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"总论文数: {len(self.results)}\n")
            f.write(f"输出目录: {self.output_dir}\n\n")
            
            f.write("分割详情:\n")
            f.write("-" * 30 + "\n")
            
            total_size = 0
            for paper in self.results:
                f.write(f"{paper['paper_number']:3d}. {paper['title']}\n")
                f.write(f"     文件: {paper['filename']}\n")
                f.write(f"     页面: {paper['start_page']}-{paper['end_page']} ({paper['total_pages']}页)\n")
                f.write(f"     大小: {paper['file_size_kb']}KB\n\n")
                total_size += paper['file_size_kb']
            
            f.write(f"\n总文件大小: {total_size/1024:.1f} MB\n")
        
        logger.info(f"📊 报告已保存: {json_file}, {txt_file}")
        return json_file, txt_file

def main():
    """主函数"""
    print("🔪 HIAT2025 PDF论文分割器")
    print("=" * 60)
    print()
    print("🚀 功能:")
    print("✅ 按页数分割PDF")
    print("✅ 智能内容分割")
    print("✅ 自动标题识别")
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
    
    print("\n🔍 选择分割方式:")
    print("1. 智能分割 (推荐 - 自动检测论文边界)")
    print("2. 按页数分割 (每6页一篇)")
    print("3. 按页数分割 (每4页一篇)")
    print("4. 按页数分割 (每8页一篇)")
    
    try:
        choice = input("\n请选择分割方式 (1/2/3/4): ").strip()
        
        # 选择要分割的文件
        if len(available_files) > 1:
            print("\n📂 选择要分割的文件:")
            for i, pdf_file in enumerate(available_files, 1):
                print(f"  {i}. {os.path.basename(pdf_file)}")
            
            file_choice = input("请选择文件 (1/2): ").strip()
            try:
                file_index = int(file_choice) - 1
                if 0 <= file_index < len(available_files):
                    pdf_path = available_files[file_index]
                else:
                    print("❌ 无效选择，使用第一个文件")
                    pdf_path = available_files[0]
            except:
                print("❌ 输入错误，使用第一个文件")
                pdf_path = available_files[0]
        else:
            pdf_path = available_files[0]
        
        print(f"\n🔪 分割文件: {pdf_path}")
        
        # 创建分割器
        splitter = SimplePDFSplitter()
        
        # 执行分割
        if choice == "1":
            print("🤖 使用智能分割模式...")
            results = splitter.split_by_content(pdf_path)
        elif choice == "2":
            print("📄 使用固定分割模式 (6页/篇)...")
            results = splitter.split_by_pages(pdf_path, 6)
        elif choice == "3":
            print("📄 使用固定分割模式 (4页/篇)...")
            results = splitter.split_by_pages(pdf_path, 4)
        elif choice == "4":
            print("📄 使用固定分割模式 (8页/篇)...")
            results = splitter.split_by_pages(pdf_path, 8)
        else:
            print("❌ 无效选择，使用智能分割")
            results = splitter.split_by_content(pdf_path)
        
        # 保存报告
        if results:
            print("\n💾 保存分割报告...")
            json_file, txt_file = splitter.save_report()
            
            # 显示结果
            print("\n" + "=" * 60)
            print("🎉 PDF分割完成！")
            print("=" * 60)
            print(f"📊 总论文数: {len(results)}")
            print(f"📁 输出目录: {splitter.output_dir}")
            
            total_size_kb = sum(p['file_size_kb'] for p in results)
            print(f"📄 总文件大小: {total_size_kb/1024:.1f} MB")
            
            print(f"\n📋 分割的论文 (前10篇):")
            for paper in results[:10]:
                print(f"  {paper['paper_number']:3d}. {paper['filename']} ({paper['total_pages']}页)")
            
            if len(results) > 10:
                print(f"  ... 还有 {len(results) - 10} 篇论文")
            
            print(f"\n🌟 分割完成！您现在可以:")
            print(f"  1. 打开 {splitter.output_dir} 目录查看分割的PDF文件")
            print(f"  2. 单独阅读每篇论文")
            print(f"  3. 查看分割报告: {txt_file}")
            print(f"  4. 根据需要重新组织文件")
        else:
            print("❌ 分割失败，没有生成任何文件")
        
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
