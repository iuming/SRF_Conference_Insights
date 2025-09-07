# SRF Conference Insights

一个用于超导射频 (SRF) 会议论文分析和可视化的综合系统。

## 🎯 项目概述

SRF Conference Insights 是一个专门设计用于处理和分析超导射频领域会议论文的系统。它能够自动提取、处理和可视化来自 IPAC、HIAT 等主要加速器物理会议的论文数据。

## ✨ 主要功能

### 📄 论文处理
- **PDF 自动提取**: 智能提取 PDF 论文的文本、图像和元数据
- **内容分析**: 深度分析论文内容，提取关键信息
- **数据结构化**: 将非结构化数据转换为结构化格式

### 🔍 会议管理
- **多会议支持**: 支持 IPAC2025、HIAT2025 等多个会议
- **数据聚合**: 统一管理不同会议的论文数据
- **状态跟踪**: 实时跟踪数据处理状态

### 📊 可视化展示
- **交互式界面**: 基于 Web 的论文浏览和搜索界面
- **统计分析**: 论文数量、作者分布等统计信息
- **图像展示**: 论文中的图表和图像展示

## 🚀 快速开始

### 环境要求
- Python 3.8+
- 现代 Web 浏览器

### 安装依赖

**推荐方式 (使用 pyproject.toml)**:
```bash
# 安装项目及其依赖
pip install -e .

# 安装开发依赖
pip install -e ".[dev]"
```

**传统方式 (使用 requirements.txt)**:
```bash
pip install -r requirements.txt
```

**手动安装核心依赖**:
```bash
pip install pandas openpyxl PyMuPDF Pillow requests beautifulsoup4 jsonschema
```

### 基本使用

1. **提取论文数据**:
```bash
python pdf_extractor.py
```

2. **运行特定会议处理**:
```bash
# IPAC2025
python conferences/run_ipac2025.py

# HIAT2025
python conferences/HIAT2025/hiat2025_extractor.py
```

3. **启动 Web 界面**:
```bash
python scripts/dev_server.py
```

然后在浏览器中访问 `http://localhost:8000`

## 📁 项目结构

```
SRF_Conference_Insights/
├── conferences/               # 会议数据处理
│   ├── IPAC2025/             # IPAC2025 会议相关
│   ├── HIAT2025/             # HIAT2025 会议相关
│   ├── aggregate/            # 聚合数据
│   └── common/               # 通用提取器
├── docs/                     # Web 前端文件
│   ├── index.html           # 主页面
│   ├── app-simple.js        # 应用逻辑
│   ├── data/                # 前端数据
│   └── images/              # 论文图像
├── scripts/                  # 工具脚本
├── .github/workflows/        # GitHub Actions
└── *.py                     # 核心处理脚本
```

## 🔧 核心组件

### PDF 处理器
- `pdf_extractor.py`: 主要的 PDF 内容提取器
- `pdf_splitter.py`: PDF 分页处理工具
- `pdf_splitter_simple.py`: 简化版分页工具

### 会议处理器
- `conference_manager.py`: 会议数据管理器
- `aggregate_conferences.py`: 多会议数据聚合
- `validate_schema.py`: 数据格式验证

### Web 界面
- `docs/index.html`: 主要的展示界面
- `docs/app-simple.js`: 前端交互逻辑
- `scripts/dev_server.py`: 开发服务器

## 📊 支持的会议

- **IPAC2025**: International Particle Accelerator Conference 2025
- **HIAT2025**: High Intensity and High Brightness Hadron Beams 2025
- 可扩展支持更多会议

## 🌐 在线演示

项目通过 GitHub Pages 自动部署：
- **在线地址**: https://iuming.github.io/SRF_Conference_Insights/
- **自动更新**: 每次推送到 main 分支后自动部署

## 📈 数据流程

1. **数据收集**: 从会议网站获取论文 PDF
2. **内容提取**: 提取文本、图像、元数据
3. **数据处理**: 清理和结构化数据
4. **聚合分析**: 多会议数据统一处理
5. **Web 展示**: 通过交互界面展示结果

## 🛠️ 开发指南

### 添加新会议支持

1. 在 `conferences/` 下创建新会议目录
2. 实现会议特定的提取器
3. 更新 `conference_schema.json`
4. 在聚合器中注册新会议

### 自定义处理逻辑

```python
from conferences.common.base_extractor import BaseExtractor

class MyConferenceExtractor(BaseExtractor):
    def extract_papers(self):
        # 实现特定的提取逻辑
        pass
```

## 📋 配置文件

- `config.json`: 主要配置文件
- `conferences/conference_schema.json`: 数据格式定义

## 🚧 项目状态

查看以下文件了解项目当前状态：
- `PROJECT_STATUS.md`: 整体项目状态
- `CONFERENCE_STATUS.md`: 各会议处理状态
- `DEPLOYMENT.md`: 部署相关信息

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目使用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 创建 Issue
- 发起 Discussion
- 提交 Pull Request

## 🙏 致谢

感谢超导射频社区和相关会议组织者提供的宝贵数据和资源。