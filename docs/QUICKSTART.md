# 🚀 快速开始指南

欢迎使用 SRF Conference Insights！这个指南将帮助您在几分钟内开始使用我们的强大功能。

## 📦 安装

### 方式一：PyPI 安装（推荐）

```bash
pip install srf-conference-insights
```

### 方式二：从源码安装

```bash
git clone https://github.com/iuming/SRF_Conference_Insights.git
cd SRF_Conference_Insights
pip install -e .
```

### 方式三：Docker 安装

```bash
docker pull iuming/srf-conference-insights:latest
docker run -p 8000:8000 iuming/srf-conference-insights
```

## 🎯 第一次使用

### 1. 启动Web界面

```bash
python scripts/dev_server.py
```

然后在浏览器中访问 `http://localhost:8000`

### 2. 处理您的第一个PDF

```python
from pdf_extractor import PDFExtractor

# 初始化提取器
extractor = PDFExtractor()

# 提取PDF内容
result = extractor.extract("your_paper.pdf")

# 查看提取结果
print(f"提取到 {len(result['pages'])} 页内容")
print(f"发现 {len(result['images'])} 张图片")
```

### 3. 分析会议数据

```python
from conferences.conference_manager import ConferenceManager

# 初始化会议管理器
manager = ConferenceManager()

# 添加新会议
manager.add_conference("IPAC2025", "/path/to/ipac/papers")

# 生成统计报告
stats = manager.generate_statistics()
print(f"总共分析了 {stats['total_papers']} 篇论文")
```

## 🔧 核心功能

### PDF内容提取

```python
from pdf_extractor import PDFExtractor

extractor = PDFExtractor()

# 高级提取配置
config = {
    "extract_images": True,
    "extract_tables": True,
    "ocr_enabled": True,
    "language": "en+zh"  # 支持英文和中文
}

result = extractor.extract("paper.pdf", config=config)
```

### 智能搜索

```python
from conferences.search_engine import SearchEngine

# 初始化搜索引擎
search = SearchEngine()

# 语义搜索
results = search.semantic_search("superconducting RF cavities")

# 过滤搜索
filtered = search.filter_by_institution("CERN")
```

### 数据可视化

```python
from conferences.visualization import DataVisualizer

viz = DataVisualizer()

# 生成机构分布图
viz.plot_institution_distribution()

# 生成主题词云
viz.generate_wordcloud()

# 导出为HTML报告
viz.export_html_report("report.html")
```

## 🌐 Web界面功能

我们的Web界面提供了强大的交互式功能：

### 📊 仪表板
- 实时统计数据
- 动态图表
- 趋势分析

### 🔍 高级搜索
- 全文搜索
- 按字段过滤
- 相关性排序

### 📄 论文浏览
- 详细信息展示
- 图片画廊
- 参考文献追踪

### 📈 数据分析
- 统计图表
- 对比分析
- 导出功能

## 🎨 自定义配置

### 配置文件

创建 `config.json` 文件：

```json
{
  "pdf_extraction": {
    "dpi": 300,
    "image_format": "PNG",
    "ocr_language": "eng+chi_sim"
  },
  "web_interface": {
    "port": 8000,
    "host": "0.0.0.0",
    "debug": false
  },
  "data_processing": {
    "max_workers": 4,
    "chunk_size": 1000,
    "cache_enabled": true
  }
}
```

### 环境变量

```bash
export SRF_CONFIG_PATH="/path/to/config.json"
export SRF_DATA_DIR="/path/to/data"
export SRF_CACHE_DIR="/path/to/cache"
```

## 🚀 高级用法

### 批量处理

```python
from conferences.batch_processor import BatchProcessor

processor = BatchProcessor()

# 批量处理多个PDF文件
results = processor.process_directory("/path/to/pdfs")

# 异步处理（推荐用于大量文件）
import asyncio

async def process_large_dataset():
    async_processor = processor.async_mode()
    results = await async_processor.process_directory("/path/to/pdfs")
    return results

results = asyncio.run(process_large_dataset())
```

### API使用

```python
from conferences.api import ConferenceAPI

# 初始化API客户端
api = ConferenceAPI(base_url="http://localhost:8000")

# 获取所有会议
conferences = api.get_conferences()

# 搜索论文
papers = api.search_papers(query="SRF technology")

# 获取统计数据
stats = api.get_statistics()
```

### 插件开发

```python
from conferences.plugins import BasePlugin

class MyCustomPlugin(BasePlugin):
    name = "my_custom_plugin"
    version = "1.0.0"
    
    def process_paper(self, paper_data):
        # 自定义处理逻辑
        enhanced_data = self.enhance_data(paper_data)
        return enhanced_data
    
    def enhance_data(self, data):
        # 实现您的增强逻辑
        return data

# 注册插件
from conferences.plugin_manager import PluginManager
manager = PluginManager()
manager.register(MyCustomPlugin())
```

## 📚 下一步

- 📖 查看 [API 文档](api.md) 了解所有可用功能
- 🎯 阅读 [最佳实践](best-practices.md) 优化使用体验
- 🔧 参考 [配置指南](configuration.md) 进行高级配置
- 🤝 查看 [贡献指南](../CONTRIBUTING.md) 参与项目开发

## ❓ 需要帮助？

- 💬 [GitHub Discussions](https://github.com/iuming/SRF_Conference_Insights/discussions)
- 🐛 [报告问题](https://github.com/iuming/SRF_Conference_Insights/issues)
- 📧 联系我们：srf-insights@example.com

---

🎉 **恭喜！您已经掌握了 SRF Conference Insights 的基本使用方法。开始探索更多强大功能吧！**
