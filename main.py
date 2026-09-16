import streamlit as st
import asyncio
import threading
import logging
import os
import sys

from routes.uaa import run_uaa_task
st.title("后台任务运行中")
st.write("点击按钮启动后台任务。若代码已修改，将自动重新加载运行。")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if "worker_started" not in st.session_state:
    st.session_state.worker_started = False

def get_code_timestamp():
    latest = 0
    for root, dirs, files in os.walk("."):
        for f in files:
            if f.endswith(".py"):
                t = os.path.getmtime(os.path.join(root, f))
                latest = max(latest, t)
    return latest

if "last_code_timestamp" not in st.session_state:
    st.session_state.last_code_timestamp = get_code_timestamp()


async def delayed_start(task_func, delay=30):
    print(f"延时 {delay} 秒启动任务: {task_func.__name__}")
    await asyncio.sleep(delay)
    try:
        return await task_func()
    except Exception as e:
        print(f"任务 {task_func.__name__} 执行失败: {e}")
        logging.error(f"任务 {task_func.__name__} 执行失败: {e}")
        raise


async def main():
    try:
        print("启动主程序，初始化所有后台任务")
    except Exception as e:
        logging.error(f"日志初始化失败: {e}")

    tasks = [
        delayed_start(run_uaa_task)
        # delayed_start(run_uaaimge_task),
        # delayed_start(run_uaaimgeup_task),
        # delayed_start(run_picb_task),
        # delayed_start(run_failed_request_task)
    ]

    for task in tasks:
        asyncio.create_task(task)

    while True:
        print("主程序运行中，等待 1 小时后检查")
        await asyncio.sleep(3600)


def start_background_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        print("程序开始运行")
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("程序被用户中断")
        logging.info("程序被用户中断")
    except Exception as e:
        print(f"程序运行出错: {e}")
        logging.error(f"程序运行出错: {e}")
    finally:
        tasks = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]
        if tasks:
            print("清理所有未完成任务")
            logging.info("清理所有未完成任务")
            try:
                loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
            except Exception as e:
                print(f"任务清理失败: {e}")
                logging.error(f"任务清理失败: {e}")
        loop.close()


if st.button("启动后台任务"):
    new_timestamp = get_code_timestamp()

    if not st.session_state.worker_started:
        st.session_state.worker_started = True
        st.session_state.last_code_timestamp = new_timestamp
        threading.Thread(target=start_background_loop, daemon=True).start()
        st.success("后台任务已启动！")
    else:
        if new_timestamp != st.session_state.last_code_timestamp:
            st.session_state.last_code_timestamp = new_timestamp
            st.warning("检测到代码已修改，正在重新加载后台任务…")
            os.execv(sys.executable, ["python"] + sys.argv)
        else:
            st.info("后台任务已在运行，且代码未修改，无需重新启动。")


if __name__ == "__main__":
    print("程序在 Streamlit 环境中运行，后台任务需通过按钮启动。")
