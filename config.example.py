"""
配置文件模板
请复制此文件为 config.py 并修改相应配置

使用方法：
1. 复制此文件：cp config.example.py config.py
2. 修改 config.py 中的配置参数
3. 运行程序：python run_crawler.py
"""

import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent

# 截图保存配置
SCREENSHOT_DIR = PROJECT_ROOT / "screenshots"
SCREENSHOT_FORMAT = "PNG"  # 截图格式：PNG, JPEG
SCREENSHOT_QUALITY = 95    # JPEG质量（1-100）

# 浏览器配置
BROWSER_HEADLESS = False   # 是否无头模式
BROWSER_WINDOW_SIZE = (1920, 1080)  # 浏览器窗口大小
BROWSER_WAIT_TIME = 3      # 页面加载等待时间（秒）

# 爬虫配置
MAX_RETRY_TIMES = 3        # 最大重试次数
RETRY_DELAY = 2           # 重试延迟（秒）
MAX_PAGES = 50            # 最大翻页数量

# ⚠️ 请修改以下配置为您的实际信息
# 目标网页配置
TARGET_URL = "https://example.com/your-target-page"  # ⚠️ 请修改为您的目标网页URL
NEXT_PAGE_SELECTOR = "cal"  # 下一页元素的ID，程序会点击该元素下的第一个A标签

# A标签点击配置
CLICK_FIRST_A_AFTER_LOGIN = False  # 是否在登录后自动点击第一个A标签

# 登录配置
LOGIN_USERNAME = "your_username"  # ⚠️ 请修改为您的登录用户名
LOGIN_WAIT_TIME = 20              # 等待用户输入密码的时间（秒）
USERNAME_INPUT_ID = "username"    # 用户名输入框的ID
LOGIN_BUTTON_WAIT = 10            # 等待登录处理的最大时间（秒）

# 智能登录检测说明：
# 1. 优先检测考勤页面关键词 -> 直接开始截图
# 2. 检测到登录关键词但找不到用户名输入框 -> 认为已登录，开始截图  
# 3. 检测到登录关键词且找到用户名输入框 -> 执行自动登录流程

# 日志配置
LOG_LEVEL = "INFO"         # 日志级别：DEBUG, INFO, WARNING, ERROR
LOG_FILE = PROJECT_ROOT / "logs" / "crawler.log"

# 确保必要目录存在
def ensure_directories():
    """确保必要的目录存在"""
    SCREENSHOT_DIR.mkdir(exist_ok=True)
    LOG_FILE.parent.mkdir(exist_ok=True)

# 初始化配置
ensure_directories() 