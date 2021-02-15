#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author: ahao
# Time: 2021/2/7 22:42
import logging
import os

from common import InitIspConfig

os.chdir(os.path.dirname(os.path.abspath(__file__)))
logFile = open("run.log", encoding="utf-8", mode="a")
logging.basicConfig(stream=logFile, format="%(asctime)s %(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)


if __name__ == "__main__":
    """
    isp-cdu疫情打卡本地版
    """
    InitIspConfig.taskPool()
