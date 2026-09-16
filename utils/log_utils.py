import logging
from colorama import Fore, Style

# 模块颜色映射
MODULE_COLORS = {
    'uaa': Fore.BLUE,
    'uaaimge': Fore.GREEN,
    'picb': Fore.MAGENTA,
    'uaaimgeup': Fore.CYAN
}

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        module_name = record.name.split('.')[-1]
        color = MODULE_COLORS.get(module_name, Fore.WHITE)
        
        message = super().format(record)
        return f"{color}{message}{Style.RESET_ALL}"

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setFormatter(ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(ch)
    
    return logger
