import asyncio
import logging
from typing import Callable, Any
from fastapi import HTTPException

async def run_background_task(
    task_name: str,
    func: Callable[[], Any],
    interval: float = 15.0
) -> None:
    """
    在后台持续运行异步任务。

    Args:
        task_name: 任务名称，用于日志记录
        func: 异步处理函数
        interval: 每次执行间隔（秒）
    """
   # logging.info(f"启动后台任务: {task_name}")
    while True:
        try:
            result = await func()
          #  print(f"{task_name} 执行结果: {result}")
        except HTTPException as e:
            logging.error(f"{task_name} HTTP 错误: {e.detail}, 状态码: {e.status_code}")
        except Exception as e:
            logging.error(f"{task_name} 执行错误: {e}")
        await asyncio.sleep(interval)

def start_background_task(task_name: str, func: Callable[[], Any], interval: float = 15.0) -> None:
    """
    启动后台任务。

    Args:
        task_name: 任务名称
        func: 异步处理函数
        interval: 执行间隔（秒）
    """
    asyncio.create_task(run_background_task(task_name, func, interval))
