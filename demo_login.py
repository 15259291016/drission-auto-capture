#!/usr/bin/env python3
"""
自动登录功能演示脚本
展示如何使用自动登录功能进行截图
"""

import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

import config
from screenshot_crawler import ScreenshotCrawler


def demo_auto_login():
    """演示自动登录功能"""
    print("🚀 DrissionPage自动登录截图演示")
    print("=" * 50)
    print(f"📋 配置信息:")
    print(f"   👤 用户名: {config.LOGIN_USERNAME}")
    print(f"   ⏰ 等待时间: {config.LOGIN_WAIT_TIME} 秒")
    print(f"   🌐 目标URL: {config.TARGET_URL}")
    print()
    
    print("🔄 智能登录检测演示流程:")
    print("1. 🌐 打开浏览器并访问目标网页")
    print("2. 🧠 智能检测当前页面状态:")
    print("   ✅ 已在考勤页面 → 直接开始截图")
    print("   ✅ 已登录状态 → 直接开始截图") 
    print("   🔐 需要登录 → 执行自动登录流程")
    print("3. 🔐 自动登录流程（仅在需要时）:")
    print("   ✍️  自动输入配置的用户名")
    print("   ⏰ 等待您手动输入密码（20秒）")
    print("   🔘 自动查找并点击登录按钮")
    print("   🔄 监控页面跳转状态")
    print("4. 📸 自动开始截图任务")
    print()
    
    confirm = input("是否开始演示？(y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("❌ 演示已取消")
        return 0
    
    try:
        print("\n🎬 开始演示...")
        
        with ScreenshotCrawler() as crawler:
            # 只截图3页作为演示
            success_count, screenshot_files = crawler.start_screenshot_task(
                url=config.TARGET_URL,
                max_pages=3
            )
            
            print(f"\n🎉 演示完成!")
            print(f"📸 成功截图: {success_count} 张")
            
            if screenshot_files:
                print(f"\n📋 截图文件:")
                for file_path in screenshot_files:
                    file_path = Path(file_path)
                    if file_path.exists():
                        print(f"   ✅ {file_path.name}")
                        
    except KeyboardInterrupt:
        print("\n⚠️  演示被用户中断")
        return 0
    except Exception as e:
        print(f"\n❌ 演示失败: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(demo_auto_login()) 