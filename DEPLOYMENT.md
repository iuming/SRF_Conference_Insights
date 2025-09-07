# GitHub Pages部署说明

## 自动部署配置

本项目已配置GitHub Actions自动部署到GitHub Pages。每当代码推送到main分支时，会自动触发构建和部署流程。

### 部署流程

1. **数据提取**: 运行PDF内容提取器，生成论文数据
2. **数据处理**: 将提取的数据转换为前端友好的JSON格式
3. **图片处理**: 复制和优化图片文件
4. **网站构建**: 准备静态网站文件
5. **部署**: 自动部署到GitHub Pages

### 启用GitHub Pages

1. 进入项目的GitHub仓库
2. 点击 `Settings` 选项卡
3. 滚动到 `Pages` 部分
4. 在 `Source` 下选择 `GitHub Actions`
5. 保存设置

### 手动触发部署

如果需要手动触发部署：

1. 进入项目的GitHub仓库
2. 点击 `Actions` 选项卡
3. 选择 `Build and Deploy HIAT2025 Analysis System` 工作流
4. 点击 `Run workflow` 按钮

### 查看部署状态

- 绿色✅: 部署成功
- 红色❌: 部署失败
- 黄色🟡: 部署中

### 访问网站

部署成功后，网站将在以下地址可用：
- https://[用户名].github.io/SRF_Conference_Insights/

### 故障排除

如果部署失败：

1. 检查GitHub Actions日志
2. 确认数据文件存在
3. 验证Python脚本无错误
4. 检查GitHub Pages设置

### 本地开发

```bash
# 启动本地服务器
python scripts/dev_server.py

# 访问 http://localhost:8000
```

### 更新数据

如果有新的PDF数据：

1. 运行 `python advanced_pdf_content_extractor.py`
2. 运行 `python scripts/prepare_data.py`
3. 提交并推送更改
4. GitHub Actions会自动重新部署
