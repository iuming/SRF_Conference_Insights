# Contributing to SRF Conference Insights

Thank you for considering contributing to SRF Conference Insights! This is a community-driven project, and we welcome all forms of contributions.

**Author**: Ming Liu <mliu@ihep.ac.cn>  
**Project**: SRF Conference Insights  
**Institution**: Institute of High Energy Physics, Chinese Academy of Sciences

## 🎯 Ways to Contribute

### 🐛 Reporting Issues
- Use [GitHub Issues](https://github.com/iuming/SRF_Conference_Insights/issues) to report bugs
- Provide detailed steps to reproduce the issue
- Include environment information (OS, Python version, etc.)
- If possible, provide error logs or screenshots

### 💡 Feature Suggestions
- Submit Feature Request Issues
- Describe the proposed feature and use cases in detail
- Explain the value this feature would bring to users

### 📝 Documentation Improvements
- Fix errors in documentation
- Add usage examples
- Translate documentation to other languages
- Improve code comments

### 🔧 Code Contributions
- Fix bugs
- Implement new features
- Optimize performance
- Add unit tests

## 🚀 Development Environment Setup

### 1. Fork and Clone Repository
```bash
# Fork the repository to your GitHub account
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/SRF_Conference_Insights.git
cd SRF_Conference_Insights
```

### 2. Setup Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install development dependencies
pip install -e ".[dev]"
```

### 3. Setup Development Tools
```bash
# Install pre-commit hooks
pre-commit install

# Run code formatting
black .

# Run type checking
mypy .

# Run unit tests
pytest
```

## 📋 Contribution Process

### 1. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-number
```

### 2. Make Changes
- Maintain consistent code style
- Add necessary tests
- Update relevant documentation
- Ensure all tests pass

### 3. Commit Changes
```bash
# Use semantic commit messages
git commit -m "feat: add new conference data extraction feature"
git commit -m "fix: resolve PDF parsing issue for large files"
git commit -m "docs: update API documentation"
```

### 4. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## 📚 Code Standards

### Python Code Style
- Use [Black](https://black.readthedocs.io/) for code formatting
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines
- Use type annotations (Type Hints)
- Functions and classes must have detailed docstrings

### Commit Message Convention
Use [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types include:
- `feat`: new feature
- `fix`: bug fix
- `docs`: documentation updates
- `style`: code formatting (no functional changes)
- `refactor`: code refactoring
- `test`: adding tests
- `chore`: build tools or auxiliary tool changes

### Testing Requirements
- New features must include unit tests
- Maintain test coverage above 80%
- All tests must pass

## 🏗️ Project Structure

```
SRF_Conference_Insights/
├── conferences/           # Conference data processing modules
│   ├── common/           # Common extractors
│   ├── IPAC2025/         # IPAC 2025 related
│   └── HIAT2025/         # HIAT 2025 related
├── docs/                 # Web frontend files
├── scripts/              # Utility scripts
├── tests/                # Unit tests
└── *.py                  # Core processing scripts
```

## 🎨 Adding New Conference Support

### 1. Create Conference Directory
```bash
mkdir conferences/YOUR_CONFERENCE
```

### 2. Implement Extractor
```python
from conferences.common.base_extractor import BaseExtractor

class YourConferenceExtractor(BaseExtractor):
    def extract_papers(self):
        # Implement conference-specific extraction logic
        pass
```

### 3. Update Configuration
- Update `conferences/conference_schema.json`
- Register new conference in `aggregate_conferences.py`

## 🚨 Troubleshooting

### Common Issues
1. **PDF extraction fails**: Check PyMuPDF version and file permissions
2. **Web interface display issues**: Verify data file format is correct
3. **Test failures**: Check dependency versions and environment variables

### Getting Help
- Check [GitHub Issues](https://github.com/iuming/SRF_Conference_Insights/issues)
- Join our [Discussions](https://github.com/iuming/SRF_Conference_Insights/discussions)
- View project [Wiki](https://github.com/iuming/SRF_Conference_Insights/wiki)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Acknowledgments

Thank you to all contributors for supporting the project! Every contribution makes the project better.

Special thanks to:
- Superconducting RF research community
- JACoW Publishing
- All users who provide feedback and suggestions

---

Thank you again for your contribution! Let's build better research tools together.
