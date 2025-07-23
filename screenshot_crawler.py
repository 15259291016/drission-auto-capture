"""
DrissionPage自动截图爬虫
主要功能：
1. 自动打开指定网页
2. 对页面进行截图
3. 自动翻页并继续截图
4. 智能文件命名和管理
"""

import sys
import time
from pathlib import Path
from typing import Optional, Tuple

from loguru import logger

try:
    from DrissionPage import WebPage
    from DrissionPage.errors import ElementNotFoundError, PageDisconnectedError
except ImportError as e:
    logger.error("请先安装DrissionPage: pip install DrissionPage")
    sys.exit(1)

import config
import utils
from utils import retry_on_failure, safe_sleep


class ScreenshotCrawler:
    """DrissionPage自动截图爬虫类"""
    
    def __init__(self, headless: bool = False):
        """
        初始化爬虫
        
        Args:
            headless: 是否使用无头模式
        """
        utils.setup_logger()
        logger.info("初始化DrissionPage自动截图爬虫...")
        
        self.headless = headless
        self.page: Optional[WebPage] = None
        self.screenshot_count = 0
        self.screenshot_dir = Path(config.SCREENSHOT_DIR)
        
        # 确保截图目录存在
        self.screenshot_dir.mkdir(exist_ok=True)
        
        # 检查磁盘空间
        if not utils.check_disk_space(self.screenshot_dir):
            logger.warning("磁盘空间可能不足，请注意")
    
    def _initialize_browser(self) -> None:
        """初始化浏览器"""
        try:
            logger.info("正在启动浏览器...")
            
            # 创建WebPage实例
            self.page = WebPage()
            
            # 设置窗口大小
            if not self.headless:
                self.page.set.window.size(*config.BROWSER_WINDOW_SIZE)
                logger.info(f"设置浏览器窗口大小: {config.BROWSER_WINDOW_SIZE}")
            
            logger.success("浏览器启动成功!")
            
        except Exception as e:
            logger.error(f"浏览器启动失败: {str(e)}")
            raise
    
    def _handle_login(self) -> bool:
        """
        处理登录页面
        
        Returns:
            bool: 是否成功处理登录
        """
        try:
            logger.info("检查是否需要登录...")
            
            page_text = self.page.html.lower()
            
            # 优先检查是否已经在目标页面或已登录状态
            if any(keyword in page_text for keyword in ["attendance", "考勤", "打卡", "签到"]):
                logger.success("检测到已在考勤页面，无需登录")
                return True
            
            # 检查是否在登录页面
            if any(keyword in page_text for keyword in ["login", "登录", "密码", "password", "username", "用户名"]):
                logger.info("检测到登录相关内容，检查是否需要登录...")
                
                # 尝试查找用户名输入框（优先使用精确的id选择器）
                username_selectors = [
                    'input[id="username"]',        # 精确匹配用户名输入框ID
                    '#username',                   # 简化的ID选择器
                    'input[name="username"]', 
                    'input[type="text"]',
                    'input[name="user"]',
                    'input[id*="user"]',
                    'input[placeholder*="用户"]',
                    'input[placeholder*="账号"]'
                ]
                
                username_input = None
                for selector in username_selectors:
                    try:
                        username_input = self.page.ele(selector)
                        if username_input:
                            break
                    except:
                        continue
                
                if username_input:
                    # 自动输入用户名
                    username_input.clear()
                    username_input.input(config.LOGIN_USERNAME)
                    logger.success(f"✅ 已自动输入用户名: {config.LOGIN_USERNAME}")
                    
                    # 提示用户输入密码并等待
                    print(f"\n🔐 请在浏览器中手动输入密码")
                    print(f"⏰ 程序将等待 {config.LOGIN_WAIT_TIME} 秒...")
                    print(f"💡 输入密码后，程序将自动点击登录按钮")
                    
                    # 等待用户输入密码
                    for i in range(config.LOGIN_WAIT_TIME):
                        print(f"\r⏳ 等待输入密码... 剩余 {config.LOGIN_WAIT_TIME - i} 秒", end="", flush=True)
                        time.sleep(1)
                        
                        # 检查是否已经登录成功（页面跳转或内容变化）
                        current_url = self.page.url
                        if config.TARGET_URL.split('?')[0] in current_url or "attendance" in current_url.lower():
                            print(f"\n🎉 检测到登录成功，页面已跳转！")
                            logger.success("登录成功，继续执行任务...")
                            return True
                    
                    print(f"\n⏰ 等待时间结束，开始查找登录按钮...")
                    
                    # 查找并点击登录按钮
                    if self._click_login_button():
                        # 等待登录处理和页面跳转
                        logger.info("等待登录处理...")
                        safe_sleep(3)
                        
                        # 再次检查是否登录成功
                        for attempt in range(config.LOGIN_BUTTON_WAIT):  # 使用配置的等待时间
                            current_url = self.page.url
                            if config.TARGET_URL.split('?')[0] in current_url or "attendance" in current_url.lower():
                                print(f"🎉 登录成功！页面已跳转到目标页面")
                                logger.success("登录成功，页面已跳转，继续执行任务...")
                                return True
                            time.sleep(1)
                            print(f"\r🔄 等待页面跳转... {attempt + 1}/{config.LOGIN_BUTTON_WAIT}", end="", flush=True)
                        
                        print(f"\n✅ 登录按钮已点击，继续执行任务...")
                        return True
                    else:
                        logger.warning("未找到登录按钮，但继续执行任务")
                        return True
                else:
                    logger.success("未找到用户名输入框，判断为已登录状态")
                    print(f"\n✅ 未检测到登录输入框，认为已经登录成功")
                    print(f"🚀 直接开始截图任务...")
                    return True
            else:
                logger.info("无需登录，直接继续")
                return True
                
        except Exception as e:
            logger.error(f"处理登录时出错: {str(e)}")
            return False

    def _click_login_button(self) -> bool:
        """
        查找并点击登录按钮
        
        Returns:
            bool: 是否成功找到并点击登录按钮
        """
        try:
            logger.info("正在查找登录按钮...")
            
            # 使用JavaScript查找包含特定文字的登录按钮
            find_login_button_script = """
            function findLoginButton() {
                // 查找所有可能的登录按钮元素
                var candidates = [];
                
                // 1. 查找提交按钮
                var submitInputs = document.querySelectorAll('input[type="submit"]');
                var submitButtons = document.querySelectorAll('button[type="submit"]');
                candidates = candidates.concat(Array.from(submitInputs), Array.from(submitButtons));
                
                // 2. 查找包含登录文字的按钮
                var allButtons = document.querySelectorAll('button, input[type="button"], a');
                for (var i = 0; i < allButtons.length; i++) {
                    var element = allButtons[i];
                    var text = (element.textContent || element.value || '').toLowerCase();
                    if (text.includes('登录') || text.includes('login') || text.includes('submit')) {
                        candidates.push(element);
                    }
                }
                
                // 3. 查找特定class或id的按钮
                var classCandidates = document.querySelectorAll('[class*="login"], [id*="login"], .login-btn, #login-btn');
                candidates = candidates.concat(Array.from(classCandidates));
                
                // 返回第一个找到的有效候选者
                for (var j = 0; j < candidates.length; j++) {
                    var candidate = candidates[j];
                    if (candidate && candidate.offsetParent !== null) { // 确保元素是可见的
                        return candidate;
                    }
                }
                
                return null;
            }
            
            return findLoginButton();
            """
            
            login_button_element = self.page.run_js(find_login_button_script)
            
            if login_button_element:
                try:
                    # 获取按钮信息用于日志
                    button_info = self.page.run_js("""
                    var el = arguments[0];
                    return {
                        tagName: el.tagName,
                        type: el.type || '',
                        text: el.textContent || el.value || '',
                        id: el.id || '',
                        className: el.className || ''
                    };
                    """, login_button_element)
                    
                    logger.info(f"找到登录按钮: {button_info}")
                    
                    # 尝试点击按钮
                    click_result = self.page.run_js("arguments[0].click(); return true;", login_button_element)
                    
                    if click_result:
                        logger.success("✅ 成功点击登录按钮")
                        return True
                    else:
                        logger.warning("点击登录按钮可能失败")
                        return False
                        
                except Exception as e:
                    logger.error(f"点击登录按钮时出错: {str(e)}")
                    return False
            else:
                logger.warning("未找到合适的登录按钮")
                
                # 尝试通过回车键提交表单
                try:
                    logger.info("尝试通过回车键提交登录表单...")
                    self.page.key.enter()
                    logger.success("✅ 已发送回车键")
                    return True
                except Exception as e:
                    logger.warning(f"发送回车键失败: {str(e)}")
                    return False
                
        except Exception as e:
            logger.error(f"查找登录按钮时出错: {str(e)}")
            return False

    @retry_on_failure(max_retries=config.MAX_RETRY_TIMES, delay=config.RETRY_DELAY)
    def _navigate_to_url(self, url: str) -> None:
        """
        导航到指定URL
        
        Args:
            url: 目标URL
        """
        logger.info(f"正在访问: {url}")
        
        if not utils.validate_url(url):
            raise ValueError(f"无效的URL格式: {url}")
        
        self.page.get(url)
        safe_sleep(config.BROWSER_WAIT_TIME)
        
        # 检查页面是否加载成功
        if "error" in self.page.title.lower() or "404" in self.page.title:
            raise Exception(f"页面加载可能失败，页面标题: {self.page.title}")
        
        logger.success(f"页面加载成功: {self.page.title}")
        
        # 处理登录
        if not self._handle_login():
            logger.warning("登录处理可能未成功，但继续执行任务")
        
        # 登录后可能需要点击第一个A标签进入正确页面
        if hasattr(config, 'CLICK_FIRST_A_AFTER_LOGIN') and config.CLICK_FIRST_A_AFTER_LOGIN:
            logger.info("配置要求登录后点击第一个A标签...")
            if self._click_first_a_tag():
                logger.success("登录后成功点击第一个A标签")
            else:
                logger.warning("登录后点击第一个A标签失败，继续执行任务")
    
    def _take_screenshot(self) -> str:
        """
        截取当前页面截图
        
        Returns:
            str: 截图文件路径
        """
        try:
            # 获取下一个截图文件名
            filename = utils.get_next_screenshot_filename(self.screenshot_dir)
            filepath = self.screenshot_dir / filename
            
            # 截图
            self.page.get_screenshot(str(filepath))
            self.screenshot_count += 1
            
            # 获取文件大小
            file_size = utils.format_file_size(filepath.stat().st_size)
            
            logger.success(f"截图保存成功: {filename} (大小: {file_size})")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"截图失败: {str(e)}")
            raise
    
    def _click_first_a_tag(self) -> bool:
        """
        点击页面中的第一个A标签
        
        Returns:
            bool: 是否成功点击第一个A标签
        """
        try:
            logger.info("正在查找第一个A标签...")
            
            # 使用JavaScript查找第一个可见的A标签
            script = """
            function findFirstATag() {
                var aTags = document.querySelectorAll('a');
                for (var i = 0; i < aTags.length; i++) {
                    var aTag = aTags[i];
                    // 检查A标签是否可见且可点击
                    if (aTag.offsetParent !== null && 
                        aTag.href && 
                        !aTag.disabled &&
                        getComputedStyle(aTag).display !== 'none') {
                        return aTag;
                    }
                }
                return null;
            }
            
            return findFirstATag();
            """
            
            first_a_element = self.page.run_js(script)
            
            if first_a_element:
                try:
                    # 获取A标签信息用于日志
                    a_info = self.page.run_js("""
                    var el = arguments[0];
                    return {
                        href: el.href || '',
                        text: el.textContent.trim() || '',
                        id: el.id || '',
                        className: el.className || ''
                    };
                    """, first_a_element)
                    
                    logger.info(f"找到第一个A标签: {a_info}")
                    
                    # 尝试点击A标签
                    click_result = self.page.run_js("arguments[0].click(); return true;", first_a_element)
                    
                    if click_result:
                        logger.success("✅ 成功点击第一个A标签")
                        safe_sleep(config.BROWSER_WAIT_TIME)
                        return True
                    else:
                        logger.warning("点击第一个A标签可能失败")
                        return False
                        
                except Exception as e:
                    logger.error(f"点击第一个A标签时出错: {str(e)}")
                    return False
            else:
                logger.warning("未找到可点击的A标签")
                return False
                
        except Exception as e:
            logger.error(f"查找第一个A标签时出错: {str(e)}")
            return False

    def _find_next_page_element(self) -> bool:
        """
        查找并点击下一页元素 - 点击ID为cal的元素下的第一个A标签
        
        Returns:
            bool: 是否找到并成功点击下一页元素
        """
        try:
            logger.info("正在查找下一页元素...")
            
            # 使用JavaScript查找cal元素下的第一个A标签
            script = f"""
            function findFirstAInCal() {{
                var calElement = document.getElementById('{config.NEXT_PAGE_SELECTOR}');
                if (!calElement) {{
                    return null;
                }}
                
                // 查找cal元素内的所有A标签
                var aTags = calElement.querySelectorAll('a');
                for (var i = 0; i < aTags.length; i++) {{
                    var aTag = aTags[i];
                    // 检查A标签是否可见且可点击
                    if (aTag.offsetParent !== null && 
                        aTag.href && 
                        !aTag.disabled &&
                        getComputedStyle(aTag).display !== 'none') {{
                        return aTag;
                    }}
                }}
                
                return null;
            }}
            
            return findFirstAInCal();
            """
            
            first_a_in_cal = self.page.run_js(script)
            
            if first_a_in_cal:
                try:
                    # 获取A标签信息用于日志
                    a_info = self.page.run_js("""
                    var el = arguments[0];
                    return {
                        href: el.href || '',
                        text: el.textContent.trim() || '',
                        id: el.id || '',
                        className: el.className || ''
                    };
                    """, first_a_in_cal)
                    
                    logger.info(f"找到cal元素下的第一个A标签: {a_info}")
                    
                    # 尝试点击A标签
                    click_result = self.page.run_js("arguments[0].click(); return true;", first_a_in_cal)
                    
                    if click_result:
                        logger.success("✅ 成功点击cal元素下的第一个A标签")
                        safe_sleep(config.BROWSER_WAIT_TIME)
                        return True
                    else:
                        logger.warning("点击cal元素下的第一个A标签可能失败")
                        return False
                        
                except Exception as e:
                    logger.error(f"点击cal元素下的第一个A标签时出错: {str(e)}")
                    return False
            else:
                logger.warning(f"未找到ID为'{config.NEXT_PAGE_SELECTOR}'的元素或其下的A标签")
                return False
                
        except Exception as e:
            logger.error(f"查找下一页元素时出错: {str(e)}")
            return False
    
    def start_screenshot_task(self, 
                            url: str, 
                            max_pages: int = 10,
                            screenshot_dir: Optional[str] = None) -> Tuple[int, list]:
        """
        开始截图任务
        
        Args:
            url: 目标网页URL
            max_pages: 最大截图页数
            screenshot_dir: 截图保存目录（可选）
            
        Returns:
            Tuple[int, list]: (成功截图数量, 截图文件路径列表)
        """
        if screenshot_dir:
            self.screenshot_dir = Path(screenshot_dir)
            self.screenshot_dir.mkdir(exist_ok=True)
        
        screenshot_files = []
        
        try:
            # 初始化浏览器
            self._initialize_browser()
            
            # 访问目标网页
            self._navigate_to_url(url)

            logger.info(f"开始截图任务，最大页数: {max_pages}")
            
            for page_num in range(1, max_pages + 1):
                try:
                    logger.info(f"正在处理第 {page_num} 页...")
                    
                    # 截图
                    screenshot_path = self._take_screenshot()
                    screenshot_files.append(screenshot_path)
                    
                    # 如果不是最后一页，尝试翻页
                    if page_num < max_pages:
                        if not self._find_next_page_element():
                            logger.info("无法找到下一页元素，可能已到最后一页")
                            break
                    
                except Exception as e:
                    logger.error(f"处理第 {page_num} 页时出错: {str(e)}")
                    continue
            
            logger.success(f"截图任务完成! 总共截图 {len(screenshot_files)} 张")
            return len(screenshot_files), screenshot_files
            
        except Exception as e:
            logger.error(f"截图任务失败: {str(e)}")
            raise
        
        finally:
            self._cleanup()
    
    def _cleanup(self) -> None:
        """清理资源"""
        try:
            if self.page:
                self.page.quit()
                logger.info("浏览器已关闭")
        except Exception as e:
            logger.warning(f"清理资源时出现警告: {str(e)}")
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self._cleanup()
    
    def click_first_a_tag(self) -> bool:
        """
        公共方法：点击页面中的第一个A标签
        
        Returns:
            bool: 是否成功点击第一个A标签
        """
        if not self.page:
            logger.error("浏览器未初始化，无法点击A标签")
            return False
        
        return self._click_first_a_tag()


def main():
    """主函数，演示如何使用爬虫"""
    try:
        # 创建爬虫实例
        with ScreenshotCrawler() as crawler:
            # 开始截图任务
            success_count, screenshot_files = crawler.start_screenshot_task(
                url=config.TARGET_URL,
                max_pages=10
            )
            
            print(f"\n✅ 任务完成!")
            print(f"📸 成功截图: {success_count} 张")
            print(f"📁 保存目录: {config.SCREENSHOT_DIR}")
            
            if screenshot_files:
                print(f"📋 截图文件列表:")
                for i, file_path in enumerate(screenshot_files, 1):
                    file_path = Path(file_path)
                    file_size = utils.format_file_size(file_path.stat().st_size)
                    print(f"   {i}. {file_path.name} ({file_size})")
            
    except KeyboardInterrupt:
        logger.info("用户中断了程序")
    except Exception as e:
        logger.error(f"程序执行失败: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 