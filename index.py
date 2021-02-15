#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author: ahao
# Time: 2021/2/7 22:42
import datetime
import json
from configparser import ConfigParser
import logging
from bs4 import BeautifulSoup
import re

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class IspService:
    """
    isp疫情信息登记服务类
    """
    def __init__(self):
        self.list = []
        self.title = None
        self.error = None
        self.content = None
        self.time = None
        self.logger = logging.getLogger()
        # 装载数据
        self.conf = self.getConfig()
        self.data = {
            'username': self.conf.get('username'),
            'userpwd': self.conf.get('userpwd'),
            'code': '',
            'login': 'login',
            'checkcode': '1',
            'rank': '0',
            'action': 'login',
            'm5': '1',
        }
        self.headers = {
            "Host": 'xsswzx.cdu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '97',
            'Origin': 'https://xsswzx.cdu.edu.cn',
            'Connection': 'close',
            "Referer": "https://xsswzx.cdu.edu.cn/ispstu/com_user/weblogin.asp",
            'Cookie': "",
            'Upgrade-Insecure-Requests': '1',
        }

    def getCookie(self):
        """
        获取cookie
        :return:
        """
        url = "https://xsswzx.cdu.edu.cn/ispstu/com_user/weblogin.asp"
        req1_headers = {
            'Host': 'xsswzx.cdu.edu.cn',
            'Connection': 'close',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
                      ',application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        }
        try:
            # 获取登录前的cookie
            # allow_redirects=False 禁止重定向， verify=false 关闭https验证
            resp = requests.get(url=url, headers=req1_headers, allow_redirects=False, verify=False)
            req1_cookie = resp.headers['Set-Cookie'].split(';')[0]
            self.headers['Cookie'] = req1_cookie
            # 查找验证码的标签
            soup = BeautifulSoup(resp.text, 'lxml')
            code = soup.find_all(id='code')[0].parent
            # 正则匹配验证码
            code = re.findall("\\d{4}", str(code))[0]
            # 装载验证码
            self.data.update({'code': code})
            # 获取登录后的Cookie
            r = requests.post(url=url, data=self.data, headers=self.headers, allow_redirects=False, verify=False)
            req2_cookie = r.headers['Set-Cookie'].split(' ')[0] + ' ' + req1_cookie
            # 更新登录后的Cookie到请求头
            self.headers['Cookie'] = req2_cookie
            self.headers['Referer'] = 'https://xsswzx.cdu.edu.cn/ispstu/com_user/webindex.asp'
            self.headers['Cache-Control'] = 'max-age=0'
            self.log('- 获取Cookie成功')
            logging.info(' - 获取Cookie成功')
        except:
            self.log('- 获取Cookie失败')
            logging.info('获取Cookie失败')
            pass


    def getClockPageUrl(self):
        """获取打卡界面的url"""
        self.getCookie()
        # 删除多余的请求头字段
        self.headers['Connection'] = 'keep-alive'
        self.headers.pop("Content-Length")
        self.headers.pop("Content-Type")
        self.headers.pop("Origin")
        url = "https://xsswzx.cdu.edu.cn/ispstu/com_user/left.asp"
        resp = requests.get(url=url, headers=self.headers, verify=False)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'lxml')
        clickPageUrl = 'https://xsswzx.cdu.edu.cn/ispstu/com_user/' + soup.find('a', string="疫情信息登记")['href']
        self.log('- 获取打卡界面的url成功')
        self.logger.info(' - 获取打卡界面的url成功')
        return clickPageUrl

    def getClockUrl(self):
        """
        获取打卡url
        :return:
        """
        clockPageUrl = self.getClockPageUrl()
        # 更新请求头Referer
        self.headers['Referer'] = 'https://xsswzx.cdu.edu.cn/ispstu/com_user/left.asp'
        self.headers.pop('Cache-Control')
        r = requests.get(url=clockPageUrl, headers=self.headers)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'lxml')
        clockUrl = 'https://xsswzx.cdu.edu.cn/ispstu/com_user/' + soup.find(value='【一键登记：无变化】').parent['href']
        self.headers['Referer'] = clockPageUrl
        self.log('- 获取打卡url成功')
        self.logger.info(' - 获取打卡url成功')
        return clockUrl

    def startClock(self):
        """
        疫情打卡入口
        :return:
        """
        self.log('- 开始疫情打卡')
        self.logger.info(' - 疫情打卡成功')
        clockUrl = self.getClockUrl()
        resp = requests.get(url=clockUrl, headers=self.headers)
        result = re.findall('提交成功', resp.content.decode('utf-8'))
        if len(result) != 0:  # 疫情打卡成功
            self.error = ''
            self.log('- 疫情打卡成功')
            self.logger.info(' - 疫情打卡成功')
            self.server()
        else:
            self.error = '疫情打卡失败'
            self.log('- 疫情打卡失败')
            self.logger.info(' - 疫情打卡失败')
            self.server()

    def log(self, text):
        """
        打印日志
        :param text:
        :return:
        """
        time_stamp = datetime.datetime.now()
        print(time_stamp.strftime('%Y.%m.%d-%H:%M:%S') + '   ' + str(text))
        self.time = time_stamp.strftime('%H:%M:%S')
        self.list.append("- [" + self.time + "]  " + str(text) + "\n\n")

    def server(self):
        """
        Server酱推送
        :return:
        """
        if self.conf['sckey'] == '':
            return
        url = 'https://sc.ftqq.com/' + self.conf['sckey'] + '.send'
        self.diyText()  # 构造发送内容
        response = requests.get(url, params={"text": self.title, "desp": self.content})
        data = json.loads(response.text)
        if data['errno'] == 0:
            self.log('- 学号:' + self.conf['username'] + '  Server酱推送成功')
            self.logger.info(' - 学号:' + self.conf['username'] + '  Server酱推送成功')
        else:
            self.log('- 学号:' + self.conf['username'] + '  Server酱推送失败,请检查sckey是否正确')
            self.logger.info(' - 学号:' + self.conf['username'] + '  Server酱推送失败,请检查sckey是否正确')

    def diyText(self):
        """
        自定义要推送到微信的内容
        title:消息的标题
        content:消息的内容,支持MarkDown格式
        """
        if self.error == '':
            state = "打卡成功"
            self.title = ("成都大学ISP打卡" + "----" + self.conf['username'])
        else:
            state = self.error
            self.title = 'isp-cdu疫情打卡异常，请自行登录网站打卡'
        self.content = (
                "------\n"
                "#### isp-cdu打卡信息\n"
                "- 学号：" + str(self.conf['username']) + "\n"
                "- 打卡状态：" + state + "\n"
                "- isp-cdu疫情打卡脚本永久免费。请勿倒卖！！！" + "\n"
                "- 脚本定制,期末项目代做(python,java,c),网课代看" + "\n"
                "- 请联系ahao，VX：CSRF5XX" + "\n"
        )

    def getConfig(self):
        """
        读取配置,配置文件为init.config
        返回字典类型的配置对象
        """
        self.log('- 开始读取配置文件')
        logging.info(' - 开始读取配置文件')
        try:
            config = ConfigParser()
            config.read('init.config', encoding='UTF-8-sig')
            username = config['token']['stuNum']
            userpwd = config['token']['password']
            sckey = config['setting']['sckey']
            self.log('- 配置文件读取完毕')
            self.logger.info(' - 配置文件读取完毕, 学号：' + username)
            conf = {
                'username': username,
                'userpwd': userpwd,
                'sckey': sckey
            }
            return conf
        except:
            self.log('- 配置文件读取失败')
            self.logger.info(' - 配置文件读取失败')
            pass


def main(event, content):
    ispService = IspService()
    ispService.startClock()