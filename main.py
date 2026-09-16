import streamlit as st
import asyncio
import threading
import logging
import os
import time

from routes.uaa import run_uaa_task

st.title("后台任务运行中")
st.write("点击按钮启动后台任务。若代码已修改，将自动重新加载后台任务。")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# -----------------------------
# 模块级变量（不需要 global）
# -----------------------------
worker_thread = None
stop_event = threading.Event()


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


# -----------------------------
# 后台任务主循环
# -----------------------------
async def main_loop():
    print("后台任务启动")
    while not stop_event.is_set():
        try:
            await run_uaa_task()
        except Exception as e:
            logging.error(f"任务执行失败: {e}")
        await asyncio.sleep(5)

    print("后台任务停止")


def start_background():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main_loop())
    loop.close()


# -----------------------------
# 启动按钮
# -----------------------------
if st.button("启动后台任务"):

    new_ts = get_code_timestamp()

    # 使用模块级变量，不需要 global
    if worker_thread is None or not worker_thread.is_alive():
        stop_event.clear()
        worker_thread = threading.Thread(target=start_background, daemon=True)
        worker_thread.start()
        st.session_state.last_code_timestamp = new_ts
        st.success("后台任务已启动！")

    else:
        if new_ts != st.session_state.last_code_timestamp:
            st.warning("检测到代码更新，正在重启后台任务…")

            stop_event.set()
            time.sleep(1)

            stop_event.clear()
            worker_thread = threading.Thread(target=start_background, daemon=True)
            worker_thread.start()

            st.session_state.last_code_timestamp = new_ts
            st.success("后台任务已重新启动！")

        else:
            st.info("后台任务已在运行，且代码未修改。")
