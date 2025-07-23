#!/usr/bin/env python3
"""
测试cal元素下第一个A标签点击功能
"""

import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

import config
from screenshot_crawler import ScreenshotCrawler


def test_cal_a_tag():
    """测试cal元素下第一个A标签点击功能"""
    print("🔗 测试cal元素下第一个A标签点击功能")
    print("=" * 50)
    print(f"📋 功能说明:")
    print(f"   🎯 查找ID为'cal'的元素")
    print(f"   🔍 在cal元素内查找第一个可点击的A标签")
    print(f"   📊 显示找到的A标签详细信息")
    print(f"   🖱️  自动点击A标签")
    print()
    
    print(f"⚙️  当前配置:")
    print(f"   📍 NEXT_PAGE_SELECTOR = '{config.NEXT_PAGE_SELECTOR}'")
    print()
    
    # 获取用户输入
    url = input(f"请输入测试URL (默认: {config.TARGET_URL}): ").strip()
    if not url:
        url = config.TARGET_URL
    
    confirm = input("是否开始测试？(y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("❌ 测试已取消")
        return 0
    
    try:
        print("\n🎬 开始测试...")
        
        with ScreenshotCrawler() as crawler:
            # 初始化并访问页面
            crawler._initialize_browser()
            crawler._navigate_to_url(url)
            
            print(f"\n🔗 测试翻页功能（cal元素下的第一个A标签）...")
            
            # 测试翻页功能
            success = crawler._find_next_page_element()
            
            if success:
                print(f"\n🎉 测试成功!")
                print(f"✅ 成功找到并点击了cal元素下的第一个A标签")
                
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
                print(f"❌ 未能找到cal元素或其下的A标签")
                print(f"💡 可能原因:")
                print(f"   - 页面中没有ID为'cal'的元素")
                print(f"   - cal元素内没有A标签")
                print(f"   - A标签被隐藏或禁用")
                print(f"   - 页面还在加载中")
                
                # 检查cal元素是否存在
                cal_exists = crawler.page.run_js(f"return document.getElementById('{config.NEXT_PAGE_SELECTOR}') !== null;")
                if cal_exists:
                    print(f"   ✅ 找到了ID为'{config.NEXT_PAGE_SELECTOR}'的元素")
                    
                    # 检查其中的A标签数量
                    a_count = crawler.page.run_js(f"""
                    var calElement = document.getElementById('{config.NEXT_PAGE_SELECTOR}');
                    return calElement ? calElement.querySelectorAll('a').length : 0;
                    """)
                    print(f"   📊 该元素内A标签数量: {a_count}")
                else:
                    print(f"   ❌ 未找到ID为'{config.NEXT_PAGE_SELECTOR}'的元素")
                
    except KeyboardInterrupt:
        print("\n⚠️  测试被用户中断")
        return 0
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(test_cal_a_tag()) 