#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author: ahao
# Time: 2021/2/7 22:42
# Description: cdu-isp 疫情打卡云函数版

from common import InitIspConfig
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def main(event, content):
    """
    isp-cdu疫情打开云函数版
    """
    InitIspConfig.taskPool()

if __name__ == '__main__':
    main(1,1)