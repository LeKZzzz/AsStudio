# -*- coding: UTF-8 -*- 
# Creator：LeK
# Date：2022/10/26

from bilibili_api import live, Credential, Danmaku
import utils
import configparser
import json
import asyncio
from modules.getweather import getweather

# 配置文件读取
config = configparser.RawConfigParser()
bilicfgpath = utils.get_path('bili')
config.read(bilicfgpath, encoding='utf-8')
credential = Credential(sessdata=config['Cookie']['sessdata'],
                        bili_jct=config['Cookie']['bili_jct'],
                        buvid3=config['Cookie']['buvid3'])
function = json.loads(open(utils.get_path("function"), encoding="utf8").read())

# 日志对象
danmaku_logger = utils.Log("danmaku")   # 弹幕
gift_logger = utils.Log("gifts")    # 礼物
welcome_logger = utils.Log("welcome")   # 入场

room_id = eval(config.items('RoomsStatus')[0][0])  # 房间id
live_danmaku = live.LiveDanmaku(room_display_id=room_id, credential=credential)  # 弹幕管理对象
live_room = live.LiveRoom(room_display_id=room_id, credential=credential)  # 直播间管理对象


# 协程被LiveDanmaku()的父类注册入了事件监听器中，收到事件名的callback之后会执行该事件对应的所有协程，协程参数event为callback_info

@live_danmaku.on('SUPER_CHAT_MESSAGE')  # 醒目留言
@live_danmaku.on('DANMU_MSG')  # 普通弹幕
async def danmaku(event):
    """
    直播间弹幕数据
    :param event: 弹幕数据
    """
    uid = event['data']['info'][2][0]
    username = event['data']['info'][2][1]
    msg = event['data']['info'][1]
    print(event['data']['info'][2][1] + ':', end=' ')
    print(event['data']['info'][1])
    str = '[UID:{}] {}: {}'.format(uid, username, msg)
    danmaku_logger.info(str)
    if function['getweather'] == True:  # 天气获取
        weather = getweather.run(msg)
        if weather != None:
            site = weather['site']
            high_temperature = weather['high_temperature']
            low_temperature = weather['low_temperature']
            weather_begin = weather['weather_begin']
            weather_end = weather['weather_end']
            weather_response = '{}今日{}转{}，气温{}到{}度'.format(site, weather_begin, weather_end, high_temperature,
                                                           low_temperature)  # 回复弹幕内容
            print(weather_response)
            weather_danmaku = Danmaku(text=weather_response)
            await live_room.send_danmaku(weather_danmaku)  # 发送天气弹幕


@live_danmaku.on('GUARD_BUY')  # 大航海续费
@live_danmaku.on('SEND_GIFT')  # 普通礼物
async def gift(event):
    """
    直播间礼物数据
    :param event: 弹幕数据
    """
    uid = event['data']['data']['uid']
    username = event['data']['data']['uname']
    giftname = event['data']['data']['giftName']
    number = event['data']['data']['num']
    str = '[UID:{}] {} 送出了"{}" x{}'.format(uid, username, giftname, number)
    gift_logger.info(str)


@live_danmaku.on("INTERACT_WORD")  # 进场用户
async def welcome(event):
    """
    直播间入场数据
    :param event:弹幕数据
    """
    uid = event['data']['data']['uid']
    username = event['data']['data']['uname']
    str = '[UID:{}] {} 进入直播间'.format(uid, username)
    welcome_logger.info(str)


def run(loop):
    loop.run_until_complete(live_danmaku.connect())
