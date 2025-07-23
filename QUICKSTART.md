# 🚀 快速启动指南

## 1️⃣ 环境准备
```bash
# 安装依赖
pip install -r requirements.txt

# 确保Chrome浏览器已安装
```

## 2️⃣ 立即启动

### 🎯 最简单方式（推荐）
```bash
python run_crawler.py
```
> 程序会提示您输入URL和页数，然后自动开始

### ⚡ 直接启动（使用默认配置）
```bash
python screenshot_crawler.py
```
> 使用config.py中的默认设置直接开始

### 🧪 测试功能
```bash
python demo_login.py        # 测试登录功能
python test_cal_a_tag.py    # 测试翻页功能
```

## 3️⃣ 运行流程
```
🔐 自动输入用户名 → ⏰ 等待您输入密码 → 📸 开始截图 → 🔗 自动翻页 → ✅ 完成
```

## 4️⃣ 输出结果
- 📸 截图保存在：`screenshots/` 目录
- 📊 日志文件在：`logs/crawler.log`  
- 📋 文件命名：`1.png`, `2.png`, `3.png`...

## 🆘 遇到问题？
查看详细文档：[README.md](README.md) 和 [USAGE.md](USAGE.md) 