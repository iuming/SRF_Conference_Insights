# Contributing to SRF Conference Insights

首先，感谢您考虑为 SRF Conference Insights 做贡献！这是一个由社区驱动的项目，我们欢迎各种形式的贡献。

## 🎯 贡献方式

### 🐛 报告问题
- 使用 [GitHub Issues](https://github.com/iuming/SRF_Conference_Insights/issues) 报告 bug
- 详细描述问题复现步骤
- 提供环境信息（操作系统、Python版本等）
- 如果可能，提供错误日志或截图

### 💡 功能建议
- 提交 Feature Request Issue
- 详细描述建议的功能和使用场景
- 说明该功能对用户的价值

### 📝 改进文档
- 修复文档中的错误
- 添加使用示例
- 翻译文档到其他语言
- 改进代码注释

### 🔧 代码贡献
- 修复 bug
- 实现新功能
- 优化性能
- 添加单元测试

## 🚀 开发环境设置

### 1. Fork 和克隆仓库
```bash
# Fork 仓库到您的 GitHub 账户
# 然后克隆您的 fork
git clone https://github.com/YOUR_USERNAME/SRF_Conference_Insights.git
cd SRF_Conference_Insights
```

### 2. 设置 Python 环境
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装开发依赖
pip install -e ".[dev]"
```

### 3. 设置开发工具
```bash
# 安装 pre-commit hooks
pre-commit install

# 运行代码格式化
black .

# 运行类型检查
mypy .

# 运行单元测试
pytest
```

## 📋 贡献流程

### 1. 创建特性分支
```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b bugfix/issue-number
```

### 2. 进行更改
- 保持代码风格一致
- 添加必要的测试
- 更新相关文档
- 确保所有测试通过

### 3. 提交更改
```bash
# 使用语义化提交消息
git commit -m "feat: add new conference data extraction feature"
git commit -m "fix: resolve PDF parsing issue for large files"
git commit -m "docs: update API documentation"
```

### 4. 推送并创建 Pull Request
```bash
git push origin feature/your-feature-name
```

然后在 GitHub 上创建 Pull Request。

## 📚 代码规范

### Python 代码风格
- 使用 [Black](https://black.readthedocs.io/) 进行代码格式化
- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 规范
- 使用类型注解 (Type Hints)
- 函数和类要有详细的文档字符串

### 提交消息规范
使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

类型包括：
- `feat`: 新功能
- `fix`: bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响代码运行）
- `refactor`: 重构
- `test`: 添加测试
- `chore`: 构建工具或辅助工具的变动

### 测试要求
- 新功能必须包含单元测试
- 保持测试覆盖率在 80% 以上
- 所有测试必须通过

## 🏗️ 项目结构

```
SRF_Conference_Insights/
├── conferences/           # 会议数据处理模块
│   ├── common/           # 通用提取器
│   ├── IPAC2025/         # IPAC 2025 相关
│   └── HIAT2025/         # HIAT 2025 相关
├── docs/                 # Web 前端文件
├── scripts/              # 工具脚本
├── tests/                # 单元测试
└── *.py                  # 核心处理脚本
```

## 🎨 添加新会议支持

### 1. 创建会议目录
```bash
mkdir conferences/YOUR_CONFERENCE
```

### 2. 实现提取器
```python
from conferences.common.base_extractor import BaseExtractor

class YourConferenceExtractor(BaseExtractor):
    def extract_papers(self):
        # 实现会议特定的提取逻辑
        pass
```

### 3. 更新配置
- 更新 `conferences/conference_schema.json`
- 在 `aggregate_conferences.py` 中注册新会议

## 🚨 问题解决

### 常见问题
1. **PDF 提取失败**: 检查 PyMuPDF 版本和文件权限
2. **Web 界面显示异常**: 确认数据文件格式正确
3. **测试失败**: 检查依赖版本和环境变量

### 获取帮助
- 查看 [GitHub Issues](https://github.com/iuming/SRF_Conference_Insights/issues)
- 加入我们的 [Discussions](https://github.com/iuming/SRF_Conference_Insights/discussions)
- 查看项目 [Wiki](https://github.com/iuming/SRF_Conference_Insights/wiki)

## 📄 许可证

通过贡献，您同意您的贡献将在 MIT 许可证下授权。

## 🙏 致谢

感谢所有贡献者对项目的支持！您的每一个贡献都让项目变得更好。

特别感谢：
- 超导射频研究社区
- JACoW Publishing
- 所有提供反馈和建议的用户

---

再次感谢您的贡献！让我们一起打造更好的科研工具。
