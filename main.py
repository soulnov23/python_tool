#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import multiprocessing

logging.basicConfig(
    filename="run.log",
    filemode="a",
    format=
    "[%(asctime)s.%(msecs)03d][%(levelname)s][%(filename)s:%(lineno)s][%(process)d]%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)


def worker(a, b):
    try:
        logging.debug(f"开始处理任务[{a} + {b}]")
    except Exception as e:
        logging.error(f"处理任务[{a} + {b}]失败: {e}")
        return e
    logging.debug(f"处理任务[{a} + {b}]成功")
    return a + b


if (__name__ == "__main__"):
    try:
        multiprocessing.set_start_method("fork", force=True)
    except Exception as e:
        logging.error("multiprocessing.set_start_method failed: %s", e)
        exit(1)

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() * 2)
    result1 = pool.apply_async(worker, (1, 2))
    result2 = pool.apply_async(worker, (3, 4))
    result3 = pool.apply_async(worker, (5, 6))

    logging.debug(f"result1: {result1.get()}")
    logging.debug(f"result2: {result2.get()}")
    logging.debug(f"result3: {result3.get()}")

    # 关闭进程池，阻止新的任务提交
    pool.close()
    # 等待所有任务完成
    pool.join()
