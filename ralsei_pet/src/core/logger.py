import logging
import os
from pathlib import Path
from datetime import datetime

class Logger:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, level=logging.INFO, log_file=None):
        if not hasattr(self, '_initialized'):
            # 配置日志文件路径
            if log_file is None:
                log_dir = Path(__file__).parent.parent.parent / "logs"
                log_dir.mkdir(exist_ok=True)
                timestamp = datetime.now().strftime("%Y-%m-%d")
                log_file = log_dir / f"pet_{timestamp}.log"
            
            # 创建日志记录器
            self.logger = logging.getLogger("RalseiPet")
            self.logger.setLevel(level)
            
            # 避免重复添加处理器
            if not self.logger.handlers:
                # 创建文件处理器
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_handler.setLevel(level)
                
                # 创建控制台处理器
                console_handler = logging.StreamHandler()
                console_handler.setLevel(level)
                
                # 设置日志格式
                formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
                file_handler.setFormatter(formatter)
                console_handler.setFormatter(formatter)
                
                # 添加处理器
                self.logger.addHandler(file_handler)
                self.logger.addHandler(console_handler)
            
            self._initialized = True
    
    def debug(self, message):
        """调试级别的日志"""
        self.logger.debug(message)
    
    def info(self, message):
        """信息级别的日志"""
        self.logger.info(message)
    
    def warning(self, message):
        """警告级别的日志"""
        self.logger.warning(message)
    
    def error(self, message):
        """错误级别的日志"""
        self.logger.error(message)
    
    def critical(self, message):
        """严重错误级别的日志"""
        self.logger.critical(message)

# 创建全局日志实例
logger = Logger()
