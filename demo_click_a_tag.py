#!/usr/bin/env python3
"""
点击第一个A标签功能演示脚本
展示如何使用点击第一个A标签的功能
"""

import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

import config
from screenshot_crawler import ScreenshotCrawler


def demo_click_first_a_tag():
    """演示点击第一个A标签功能"""
    print("🔗 点击第一个A标签功能演示")
    print("=" * 50)
    print(f"📋 功能说明:")
    print(f"   🎯 自动查找页面中第一个可点击的A标签")
    print(f"   🔍 智能过滤隐藏和无效的A标签")
    print(f"   📊 显示A标签的详细信息")
    print(f"   🖱️  自动点击找到的A标签")
    print()
    
    # 获取用户输入
    url = input(f"请输入测试URL (默认: {config.TARGET_URL}): ").strip()
    if not url:
        url = config.TARGET_URL
    
    print(f"\n📋 测试配置:")
    print(f"   🌐 目标URL: {url}")
    print()
    
    confirm = input("是否开始测试点击第一个A标签？(y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("❌ 测试已取消")
        return 0
    
    try:
        print("\n🎬 开始测试...")
        
        with ScreenshotCrawler() as crawler:
            # 初始化并访问页面
            crawler._initialize_browser()
            crawler._navigate_to_url(url)
            
            print(f"\n🔗 测试点击第一个A标签功能...")
            
            # 点击第一个A标签
            success = crawler.click_first_a_tag()
            
            if success:
                print(f"\n🎉 测试成功!")
                print(f"✅ 第一个A标签已被成功点击")
                
                # 等待页面响应
                import time
                print(f"⏰ 等待页面响应...")
                time.sleep(3)
                
                # 可选：截图查看结果
                save_screenshot = input("是否截图查看结果？(y/N): ").strip().lower()
                if save_screenshot in ['y', 'yes']:
                    screenshot_path = crawler._take_screenshot()
                    print(f"📸 截图已保存: {screenshot_path}")
                    
            else:
                print(f"\n⚠️  测试失败")
                print(f"❌ 未能找到或点击第一个A标签")
                print(f"💡 可能原因:")
                print(f"   - 页面中没有可点击的A标签")
                print(f"   - A标签被隐藏或禁用")
                print(f"   - 页面还在加载中")
                
    except KeyboardInterrupt:
        print("\n⚠️  测试被用户中断")
        return 0
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(demo_click_first_a_tag()) 