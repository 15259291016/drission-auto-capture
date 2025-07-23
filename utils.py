"""
工具函数模块
包含项目中使用的各种辅助函数
"""

import os
import time
from pathlib import Path
from typing import Optional, Union

import config
from loguru import logger


def setup_logger() -> None:
    """设置日志器配置"""
    # 移除默认的logger
    logger.remove()
    
    # 添加控制台输出
    logger.add(
        sink=lambda msg: print(msg, end=""),
        level=config.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
               "<level>{message}</level>",
        colorize=True
    )
    
    # 添加文件输出
    logger.add(
        config.LOG_FILE,
        level=config.LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="10 MB",
        retention="7 days",
        encoding="utf-8"
    )


def get_next_screenshot_filename(screenshot_dir: Union[str, Path]) -> str:
    """
    获取下一个截图文件名
    
    Args:
        screenshot_dir: 截图保存目录
        
    Returns:
        str: 下一个截图文件名（如: "1.png", "2.png"等）
    """
    screenshot_dir = Path(screenshot_dir)
    screenshot_dir.mkdir(exist_ok=True)
    
    # 查找现有截图文件的最大编号
    max_index = 0
    for file in screenshot_dir.glob("*.png"):
        try:
            index = int(file.stem)
            max_index = max(max_index, index)
        except ValueError:
            continue
    
    # 返回下一个编号的文件名
    next_index = max_index + 1
    return f"{next_index}.png"


def safe_sleep(seconds: float) -> None:
    """
    安全的睡眠函数，包含日志记录
    
    Args:
        seconds: 睡眠时间（秒）
    """
    logger.debug(f"等待 {seconds} 秒...")
    time.sleep(seconds)


def validate_url(url: str) -> bool:
    """
    验证URL格式是否正确
    
    Args:
        url: 待验证的URL
        
    Returns:
        bool: URL是否有效
    """
    import re
    url_pattern = re.compile(
        r'^https?://'  # http:// 或 https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # 域名
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # 可选端口
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(url_pattern.match(url))


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """
    重试装饰器
    
    Args:
        max_retries: 最大重试次数
        delay: 重试延迟时间
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(f"第 {attempt + 1} 次尝试失败: {str(e)}, {delay} 秒后重试...")
                        safe_sleep(delay)
                    else:
                        logger.error(f"所有 {max_retries + 1} 次尝试都失败了")
                        
            # 如果所有重试都失败，抛出最后一个异常
            raise last_exception
            
        return wrapper
    return decorator


def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小显示
    
    Args:
        size_bytes: 文件大小（字节）
        
    Returns:
        str: 格式化后的文件大小
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024.0 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def check_disk_space(path: Union[str, Path], min_free_gb: float = 1.0) -> bool:
    """
    检查磁盘剩余空间
    
    Args:
        path: 检查路径
        min_free_gb: 最小剩余空间（GB）
        
    Returns:
        bool: 是否有足够空间
    """
    try:
        import shutil
        free_bytes = shutil.disk_usage(path).free
        free_gb = free_bytes / (1024 ** 3)
        
        if free_gb < min_free_gb:
            logger.warning(f"磁盘剩余空间不足: {free_gb:.1f} GB (需要至少 {min_free_gb} GB)")
            return False
        
        return True
    except Exception as e:
        logger.error(f"检查磁盘空间时出错: {str(e)}")
        return False 