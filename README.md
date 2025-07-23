# Drission Auto Capture

> 🤖 **智能网页自动截图爬虫** | 基于DrissionPage的自动化截图工具
> 
> 📚 **快速上手**: [点击查看快速启动指南 →](QUICKSTART.md) | 🔒 **安全说明**: [安全配置指南 →](SECURITY.md)

## 项目描述
**Drission Auto Capture** 是一个基于DrissionPage框架的智能网页自动截图工具。支持自动登录检测、智能翻页、批量截图等功能。特别适用于需要定期截图保存网页内容的场景，如管理系统、报表系统、监控面板等。

## 功能特性
- 🌐 自动打开指定网页
- 🧠 **智能登录检测**（自动判断登录状态，已登录直接截图，需要登录自动完成）
- 🔐 **完全自动登录**（自动输入用户名 → 等待密码输入 → 自动点击登录 → 检测跳转）
- 🔗 **智能A标签点击**（支持翻页、登录后操作、手动调用等多种场景）
- 📸 自动截图保存（支持命名序号递增）
- 🔄 智能自动翻页
- 📁 智能文件管理
- 🛡️ 完善的错误处理和日志记录

## 环境要求
- Python 3.8+
- DrissionPage库
- 支持Chrome浏览器

## 📦 环境准备

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 确保Chrome浏览器已安装
程序需要Chrome浏览器支持，请确保系统中已安装Chrome。

### 3. 配置参数（必需）
⚠️ **首次使用前必须配置**：
```bash
# 复制配置模板
cp config.example.py config.py

# 编辑配置文件，修改以下关键参数：
# - TARGET_URL: 您的目标网页地址  
# - LOGIN_USERNAME: 您的登录用户名
```

在 `config.py` 中可以修改以下设置：
```python
# 目标网页
TARGET_URL = "https://example.com/your-target-page"  # 修改为您的目标网页

# 登录信息  
LOGIN_USERNAME = "your_username"  # 修改为您的用户名
LOGIN_WAIT_TIME = 20              # 等待输入密码的时间

# 截图设置
SCREENSHOT_DIR = "screenshots"    # 截图保存目录
MAX_PAGES = 50                    # 最大翻页数量

# 翻页设置
NEXT_PAGE_SELECTOR = "cal"        # 翻页元素ID
```

## 🚀 快速启动

### 方法一：交互式启动（推荐新手）
```bash
python run_crawler.py
```
程序会提示您输入URL和截图页数，然后自动开始任务。

### 方法二：直接启动（使用默认配置）
```bash
python screenshot_crawler.py
```
直接使用配置文件中的默认设置开始截图任务。

### 方法三：测试功能
```bash
# 测试登录功能
python demo_login.py

# 测试A标签点击功能  
python demo_click_a_tag.py

# 测试cal元素下A标签点击
python test_cal_a_tag.py
```

## 📋 详细使用方法

### 代码调用方式
```python
from screenshot_crawler import ScreenshotCrawler

# 创建爬虫实例
crawler = ScreenshotCrawler()

# 开始截图任务
crawler.start_screenshot_task(
    url="https://example.com/your-target-page",
    max_pages=10  # 最大截图页数
)
```

### 自定义配置启动
```python
from screenshot_crawler import ScreenshotCrawler

# 使用自定义参数
with ScreenshotCrawler() as crawler:
    success_count, screenshot_files = crawler.start_screenshot_task(
        url="your_target_url",
        max_pages=20,
        screenshot_dir="./my_screenshots"
    )
    print(f"截图完成，共 {success_count} 张")
```

## 🔄 运行流程

程序启动后将按以下步骤执行：

### 1. 初始化阶段
```
🚀 启动浏览器
🌐 访问目标网页
🔍 智能检测页面状态
```

### 2. 登录处理（如需要）
```
🔐 自动输入用户名: your_username
⏰ 等待您手动输入密码（20秒）
🔘 自动点击登录按钮
🔄 等待页面跳转
```

### 3. 截图和翻页
```
📸 对当前页面截图 (1.png)
🔗 查找cal元素下的第一个A标签
🖱️  点击A标签翻页
📸 对新页面截图 (2.png)
🔄 重复直到完成...
```

### 4. 任务完成
```
✅ 显示截图统计信息
📁 列出所有截图文件
🎉 任务完成
```

### 参数说明
- `url`: 目标网页地址
- `max_pages`: 最大截图页数（默认为10）
- `screenshot_dir`: 截图保存目录（默认为screenshots）
- `wait_time`: 页面加载等待时间（默认为3秒）

## 📁 项目文件结构
```
selenium_demo/
├── README.md                 # 📖 项目说明文档
├── USAGE.md                  # 📚 详细使用指南
├── requirements.txt          # 📦 依赖包列表
├── run_crawler.py           # 🎯 主要运行脚本（推荐）
├── screenshot_crawler.py     # 🤖 核心爬虫代码
├── config.py                # ⚙️ 配置文件
├── utils.py                 # 🔧 工具函数
├── demo_login.py            # 🎬 登录功能演示
├── demo_click_a_tag.py      # 🔗 A标签点击演示
├── test_cal_a_tag.py        # 🧪 cal元素A标签测试
├── screenshots/             # 📸 截图保存目录
└── logs/                    # 📊 日志文件目录
```

### 🎯 核心文件说明
- **`run_crawler.py`** - 最简单的启动方式，交互式操作
- **`screenshot_crawler.py`** - 核心爬虫实现，包含所有主要功能
- **`config.py`** - 配置文件，可自定义各种参数
- **`demo_*.py`** - 各种功能的演示和测试脚本

## ⚠️ 注意事项
1. **登录要求**: 需要手动输入密码完成登录
2. **浏览器支持**: 确保Chrome浏览器已安装
3. **网络稳定**: 保持稳定的网络连接
4. **合规使用**: 遵守网站使用条款

## 🛠️ 故障排除

### 常见问题

#### 1. 程序启动失败
```bash
# 错误：找不到Chrome浏览器
解决：安装Chrome浏览器或检查安装路径

# 错误：模块导入失败
解决：pip install -r requirements.txt
```

#### 2. 登录相关问题
```bash
# 找不到用户名输入框
解决：检查网页是否正确加载，或修改用户名输入框选择器

# 登录后无法进入目标页面
解决：检查登录凭据或网络连接
```

#### 3. 截图和翻页问题
```bash
# 找不到cal元素
解决：确认页面结构，检查NEXT_PAGE_SELECTOR配置

# 截图失败
解决：检查磁盘空间和写入权限
```

### 📊 调试方法
```bash
# 查看详细日志
查看 logs/crawler.log 文件

# 测试特定功能
python demo_login.py        # 测试登录
python test_cal_a_tag.py    # 测试翻页
```

## 🔧 错误处理机制
- ✅ 自动重试机制（失败时重试3次）
- ✅ 详细的错误日志记录
- ✅ 优雅的异常处理和资源清理
- ✅ 智能状态检测和恢复

## 开发计划
- [ ] 支持多种浏览器
- [ ] 添加图片压缩功能
- [ ] 支持批量URL处理
- [ ] 添加GUI界面 