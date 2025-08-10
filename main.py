#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import multiprocessing
import schedule
import sys
import signal
import time

logging.getLogger().setLevel(logging.DEBUG)
file_handler = logging.FileHandler(
    filename="run.log",
    mode="a",
    encoding="utf-8",
)
file_handler.setFormatter(
    logging.Formatter(
        "[%(asctime)s.%(msecs)03d][%(levelname)s][%(filename)s:%(lineno)s][%(process)d]%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
file_handler.setLevel(logging.DEBUG)
logging.getLogger().addHandler(file_handler)
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter(
        "[%(asctime)s.%(msecs)03d][%(levelname)s][%(filename)s:%(lineno)s][%(process)d]%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
console_handler.setLevel(logging.DEBUG)
logging.getLogger().addHandler(console_handler)

pool = None


def worker():
    global pool
    if pool is None:
        logging.error("进程池未初始化")
        return

    result = pool.apply_async(actual_worker)
    result.get()


def actual_worker():
    pass


def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


if (__name__ == "__main__"):
    try:
        multiprocessing.set_start_method("fork", force=True)
    except Exception as e:
        logging.error("multiprocessing.set_start_method failed: %s", e)
        sys.exit(1)

    pool = multiprocessing.Pool(
        processes=multiprocessing.cpu_count() * 2,
        initializer=init_worker,
    )

    schedule.every(3).seconds.do(worker)
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
            logging.info("定时任务调度器运行中...")
    except KeyboardInterrupt:
        logging.info("收到中断信号，正在退出...")
    except Exception as e:
        logging.error("schedule failed: %s", e)
    finally:
        if pool:
            logging.info("正在关闭进程池...")
            pool.terminate()
            pool.join()
            logging.info("进程池已关闭")
        logging.info("程序已退出")
        sys.exit(0)
