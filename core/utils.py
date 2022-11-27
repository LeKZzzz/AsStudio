# -*- coding: UTF-8 -*- 
# Creator：LeK
# Date：2022/10/14
"""

通用工具库

"""

import os
import json
from bilibili_api import live
import time
import logging



def get_path(field: str):
    """
    获取配置文件路径

    Args:
        需要获取的配置文件

    Returns:
        配置文件路径
    """
    pathindex = os.path.join(os.path.dirname(__file__), "path.json")
    if os.path.exists(pathindex):
        with open(pathindex, encoding="utf8") as f:
            return os.path.join(os.path.dirname(__file__), '..', json.loads(f.read())[field])


async def get_room_info(room_id: int):
    """
    直播间信息获取
    :param room_id: 房间号
    :return: 房间信息
    """
    result = {}
    request = live.LiveRoom(room_id)
    room_info = await request.get_room_info()
    nickname = room_info['anchor_info']['base_info']['uname']
    roomtitle = room_info['room_info']['title']
    result['nickname'] = nickname
    result['roomtitle'] = roomtitle
    return result


class Log:
    """
    日志类
    """

    def __init__(self, module: str):
        """
        初始化日志类
        :param module:调用的模块名，用于生成日志文件路径
        """
        self.pretime = self.curtime = time.localtime()  # 时间检测
        self.prepath = get_path(module)
        self.filename = self.prepath + str(self.curtime[0]) + '-' + str(self.curtime[1]) + '-' + str(
            self.curtime[2]) + '.txt'  # 日志文件的绝对路径
        # 初始化Logger对象
        self.logger = logging.Logger(name='module')
        self.logger.setLevel(logging.DEBUG)
        if not os.path.exists(self.filename):  # 检查日志文件
            self.file = open(self.filename, 'w')
            self.file.close()
        self.handler = logging.FileHandler(filename=self.filename, mode='a', encoding='utf-8')
        self.handler.setLevel(logging.INFO)
        self.formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def info(self, info: str):
        """
        生成正常运行日志
        :param info:日志信息
        """
        self.filecheck()
        self.logger.info(info)

    def exception(self):
        """
        生成错误运行日志
        """
        self.filecheck()
        self.logger.exception('Exception occurred')

    def filecheck(self):
        """
        以日为单位，检查是否需要新建日志文件
        """
        self.curtime = time.localtime()
        if self.curtime[2] > self.pretime[2]:
            self.filename = self.prepath + str(self.curtime[0]) + '-' + str(self.curtime[1]) + '-' + str(
                self.curtime[2]) + '.txt'
            self.sethandler()
            self.pretime = self.curtime

    def sethandler(self):
        """
        新建日志文件，重新设置处理器
        """
        self.file = open(self.filename, 'w')
        self.file.close()
        self.logger.removeHandler(self.handler)
        self.handler = logging.FileHandler(filename=self.filename, mode='a', encoding='utf-8')
        self.handler.setLevel(logging.INFO)
        self.formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)


def read_json(filepath):  # 读取json数据
    with open(filepath, 'r', encoding='utf8') as fp:
        data = json.load(fp)
        return data


def write_json(data, filepath): # 写入json数据
    with open(filepath, 'w', encoding='utf8') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4)