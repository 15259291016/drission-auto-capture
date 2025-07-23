#!/usr/bin/env python3
"""
DrissionPage自动截图爬虫 - 运行脚本
使用方法：python run_crawler.py
"""

import sys
from pathlib import Path

from utils import safe_sleep

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

import config
from screenshot_crawler import ScreenshotCrawler


def main():
    """主运行函数"""
    print("🚀 DrissionPage自动截图爬虫")
    print("=" * 50)
    
    # 获取用户输入
    url = input(f"请输入网页URL (默认: {config.TARGET_URL}): ").strip()
    if not url:
        url = config.TARGET_URL
    
    max_pages_input = input("请输入最大截图页数 (默认: 10): ").strip()
    try:
        max_pages = int(max_pages_input) if max_pages_input else 10
    except ValueError:
        print("⚠️  输入的页数无效，使用默认值 10")
        max_pages = 10
    
    print(f"\n📋 任务配置:")
    print(f"   🌐 目标URL: {url}")
    print(f"   📄 最大页数: {max_pages}")
    print(f"   📁 保存目录: {config.SCREENSHOT_DIR}")
    print()
    
    # 确认开始
    confirm = input("是否开始截图任务？(y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("❌ 任务已取消")
        return 0
    try:
        # 创建爬虫实例并开始任务
        with ScreenshotCrawler() as crawler:
            success_count, screenshot_files = crawler.start_screenshot_task(
                url=url,
                max_pages=max_pages
            )
            
            print(f"\n🎉 任务完成!")
            print(f"📸 成功截图: {success_count} 张")
            print(f"📁 保存目录: {config.SCREENSHOT_DIR}")
            
            if screenshot_files:
                print(f"\n📋 截图文件列表:")
                for i, file_path in enumerate(screenshot_files, 1):
                    file_path = Path(file_path)
                    if file_path.exists():
                        file_size = file_path.stat().st_size
                        size_str = f"{file_size / 1024:.1f} KB" if file_size < 1024*1024 else f"{file_size / (1024*1024):.1f} MB"
                        print(f"   {i}. {file_path.name} ({size_str})")
            
            print(f"\n💡 提示: 可以在 {config.SCREENSHOT_DIR} 目录中查看所有截图")
            
    except KeyboardInterrupt:
        print("\n⚠️  用户中断了程序")
        return 0
    except Exception as e:
        print(f"\n❌ 程序执行失败: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 