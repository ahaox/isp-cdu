#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author: ahao
# Time: 2021/2/15 12:06
import json
import logging
from configparser import ConfigParser
import time

from spider import IspService
logger = logging.getLogger()


class InitIspConfig:
    """
    init初始化配置
    """

    @staticmethod
    def loadJson(jsonPath):
        """
        加载Json文件
        jsonPath:json文件的名字,例如account.json
        """
        with open(jsonPath, encoding='utf-8') as f:
            account = json.load(f)
        return account

    @staticmethod
    def taskPool():
        """
        任务池
        """
        config = InitIspConfig.getConfig()
        if config['peopleSwitch'] is True:
            logger.info('多人开关已打开,即将执行进行多人任务\n========================================')
            IspService.log('多人开关已打开,即将执行进行多人任务\n========================================')
            account = InitIspConfig.loadJson("account.json")
            for man in account:
                logger.info('学号: ' + man['stuNum'] + '  开始执行')
                IspService.log('学号: ' + man['stuNum'] + '  开始执行')
                task = IspService(man['stuNum'], man['password'], man['sckey'])
                task.startClock()
                time.sleep(10)
            logger.info('所有账号已全部完成任务,服务进入休眠中,等待明天重新启动')
            IspService.log('所有账号已全部完成任务,服务进入休眠中,等待明天重新启动')
        else:
            logger.info('学号: ' + config['stuNum'] + '  开始执行')
            IspService.log('学号: ' + config['stuNum'] + '  开始执行')
            task = IspService(config['stuNum'], config['password'], config['sckey'])
            task.startClock()

    @staticmethod
    def getConfig():
        """
        读取配置,配置文件为init.config
        返回字典类型的配置对象
        """
        config = ConfigParser()
        config.read('config.ini', encoding='UTF-8-sig')
        stuNum = config['token']['stuNum']
        password = config['token']['password']
        peopleSwitch = config.getboolean('setting', 'peopleSwitch')
        sckey = config['setting']['sckey']
        logger.info('配置文件读取完毕')
        IspService.log('配置文件读取完毕')
        conf = {
            'stuNum': stuNum,
            'password': password,
            'peopleSwitch': peopleSwitch,
            'sckey': sckey
        }
        return conf
