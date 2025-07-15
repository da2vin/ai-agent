#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import time
import logging
import datetime
from logging.handlers import TimedRotatingFileHandler


class TaskLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        task_id = kwargs.pop('task_id', 'system') or 'system'
        prefix = f'[task_id: {task_id}]'
        return f'{prefix} - {msg}', kwargs


# https://docs.python.org/zh-cn/3.8/howto/logging.html
def get_logger(name):
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter(
        f'[ab] - [{name}] - [{os.getenv("ENV")}] %(asctime)s - %(process)d - %(thread)s - %(filename)s - %(funcName)s - [line:%(lineno)d] - %(levelname)s: %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    # add file handler
    log_dir = os.path.dirname(__file__) + "/../logs/" + name

    try:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
    except Exception as e:
        pass

    # today = datetime.datetime.today().strftime("%Y-%m-%d")
    abs_file_name = os.path.join(log_dir, f"{name}.log")
    file_handler = TimedRotatingFileHandler(filename=abs_file_name, when='midnight', backupCount=3, encoding="utf8")
    file_handler.suffix = "%Y-%m-%d"

    # file_handler.suffix = "%Y-%m-%d.log"
    # file_handler.extMatch = r"^\d{4}-\d{2}-\d{2}\.log$"
    # file_handler.extMatch = re.compile(file_handler.extMatch, re.ASCII)

    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    return TaskLoggerAdapter(logger)


if __name__ == '__main__':
    mlogger = get_logger("Test")
    index = 0
    while True:
        index += 1
        mlogger.info("index", task_id="88888")
        time.sleep(1)
