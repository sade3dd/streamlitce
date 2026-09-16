import json
import io
import asyncio
import logging
from contextlib import asynccontextmanager
import gc
import random
import time
from utils.task_scheduler import start_background_task
from utils.log_utils import get_logger
logger = get_logger(__name__)
task_started = False

# Picb.cc API 密钥和相册ID轮询配置

async def process_uaa(id1: str = '1') -> dict:
    logger.info(f"开始处理 KKXISJJXUIUIS 任务，参数 id1={id1}")
    
    result = {"message": "KKXISJJXUIUIS 任务执行成功"}
    logger.info(f"KKXISJJXUIUIS 任务执行成功 | id1={id1} | result={result}")
    
    return result

async def run_uaa_task():    
    global task_started
    try:
        if not task_started:
            start_background_task("UAA Task", lambda: process_uaa(2), interval=10.0)
            task_started = True
            return {"message": "UAA 后台任务已启动"}
        else:
            return {"message": "UAA 后台任务已在运行"}
    except Exception as e:
        logger.error(f"启动 UAA 任务失败: {str(e)}", exc_info=True)
        return {"message": "启动 UAA 任务失败"}

async def start_uaa_task():
    global task_started
    try:
        if not task_started:
            start_background_task("UAA Task", lambda: process_uaa(2))
            task_started = True
            return {"message": "UAA 后台任务已启动"}
        else:
            return {"message": "UAA 后台任务已在运行"}
    except Exception as e:
        logger.error(f"启动 UAA 任务失败: {str(e)}", exc_info=True)
        return {"message": "启动 UAA 任务失败"}
