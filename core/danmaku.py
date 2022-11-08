# -*- coding: UTF-8 -*- 
# Creator：LeK
# Date：2022/10/26

from bilibili_api import live, Credential
import utils
import configparser
import asyncio

# 配置文件读取
config = configparser.RawConfigParser()
bilicfgpath = utils.get_path('bili')
config.read(bilicfgpath, encoding='utf-8')
credential = Credential(sessdata=config['Cookie']['sessdata'],
                        bili_jct=config['Cookie']['bili_jct'],
                        buvid3=config['Cookie']['buvid3'])

# 直播间上一次查询时的状态
prestatus = [eval(status[1]) for status in config.items('RoomsStatus')]

# 日志对象
danmaku_logger = utils.Log("danmaku")
gift_logger = utils.Log("gifts")

room_id = eval(config.items('RoomsStatus')[0][0])
room = live.LiveDanmaku(room_display_id=room_id, credential=credential)


@room.on('DANMU_MSG')  # 协程被LiveDanmaku()的父类注册入了事件监听器中，收到事件名的callback之后会执行该事件对应的所有协程，协程参数event为callback_info
async def on_danmaku(event):
    # 收到弹幕
    print(event['data']['info'][2][1] + ':', end=' ')
    print(event['data']['info'][1])
    str = '[UID:{}]{}:{}'.format(event['data']['info'][2][0],event['data']['info'][2][1], event['data']['info'][1])
    danmaku_logger.info(str)


@room.on('SEND_GIFT')
async def on_gift(event):
    # 收到礼物
    str = '[UID:{}]{}送出了"{}" x{}'.format(event['data']['data']['uid'], event['data']['data']['uname'],
                                         event['data']['data']['giftName'], event['data']['data']['num'])
    gift_logger.info(str)


def run(loop):

    loop.run_until_complete(room.connect())

