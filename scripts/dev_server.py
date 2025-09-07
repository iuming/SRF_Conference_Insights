#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地开发服务器
用于测试GitHub Pages网站
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

def start_server():
    """启动本地开发服务器"""
    
    # 切换到docs目录
    docs_dir = Path("docs")
    if not docs_dir.exists():
        print("❌ docs目录不存在，请先运行数据处理脚本")
        return
    
    os.chdir(docs_dir)
    
    # 服务器配置
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    
    # 启动服务器
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🌐 启动本地开发服务器...")
        print(f"📍 服务器地址: http://localhost:{PORT}")
        print(f"📁 服务目录: {docs_dir.absolute()}")
        print(f"⏹️  按 Ctrl+C 停止服务器")
        print("-" * 50)
        
        # 自动打开浏览器
        try:
            webbrowser.open(f"http://localhost:{PORT}")
            print("🔗 已自动打开浏览器")
        except:
            print("💡 请手动打开浏览器访问上述地址")
        
        print("-" * 50)
        print("🚀 服务器运行中...")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n⏹️  服务器已停止")

if __name__ == "__main__":
    start_server()
