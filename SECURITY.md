# 🔒 安全说明

## 敏感信息保护

为了保护您的隐私和安全，本项目采用了以下安全措施：

### 📋 不会同步到Git的信息

- ✅ `config.py` - 您的实际配置文件（包含敏感信息）
- ✅ `.env` - 环境变量文件
- ✅ `screenshots/*.png` - 截图文件
- ✅ `logs/*.log` - 日志文件
- ✅ `.venv/` - 虚拟环境
- ✅ `__pycache__/` - Python缓存

### 📋 会同步到Git的信息

- ✅ `config.example.py` - 配置模板（不含敏感信息）
- ✅ 源代码文件
- ✅ 文档文件
- ✅ `screenshots/.gitkeep` - 目录结构保持文件

## 🚀 首次使用配置

1. **复制配置模板**：
   ```bash
   cp config.example.py config.py
   ```

2. **编辑配置文件**：
   ```python
   # 修改以下参数为您的实际信息
   TARGET_URL = "https://your-actual-website.com"
   LOGIN_USERNAME = "your_actual_username"
   ```

3. **确认.gitignore生效**：
   ```bash
   git status
   # 确认 config.py 不在待提交列表中
   ```

## ⚠️ 重要提醒

- ❌ **绝对不要** 将真实的用户名、密码、内部URL提交到公开仓库
- ✅ **务必检查** 提交前的文件列表，确保不包含敏感信息
- ✅ **定期审查** .gitignore 文件，确保敏感文件被正确忽略
- ✅ **使用环境变量** 来存储敏感配置（推荐）

## 🔧 环境变量方式（推荐）

可以通过环境变量来配置敏感信息：

```python
import os

# 在 config.py 中使用环境变量
TARGET_URL = os.getenv("TARGET_URL", "https://example.com/default")
LOGIN_USERNAME = os.getenv("LOGIN_USERNAME", "default_user")
```

```bash
# 在系统中设置环境变量
export TARGET_URL="https://your-actual-website.com"
export LOGIN_USERNAME="your_actual_username"
```

## 📞 如发现安全问题

如果您发现任何安全相关问题，请：

1. **不要** 在公开的Issue中报告
2. 直接联系项目维护者
3. 提供详细的问题描述和复现步骤

---

> 🛡️ **安全是大家的责任**，感谢您的配合！ 