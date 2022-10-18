# -*- coding: UTF-8 -*- 
# Creator：LeK
# Date：2022/10/13


from bilibili_api import dynamic, Credential, live
import asyncio
import configparser
import time
import utils

# 配置文件读取
config = configparser.RawConfigParser()
bilicfgpath = utils.get_path('bili')
config.read(bilicfgpath, encoding='utf-8')
credential = Credential(sessdata=config['Cookie']['sessdata'],
                        bili_jct=config['Cookie']['bili_jct'],
                        buvid3=config['Cookie']['buvid3'])

# 直播间上一次查询时的状态
prestatus = [eval(status[1]) for status in config.items('RoomsStatus')]


async def send_dynamic(num):
    """
    开播发送开播b站动态
    """
    global dynamic_id
    room = config.items('RoomsStatus')[num][0]
    request = live.LiveRoom(eval(room))
    room_info = await request.get_room_info()
    nickname = room_info['anchor_info']['base_info']['uname']
    roomtitle = room_info['room_info']['title']
    text = '哔哩哔哩开播小喇叭：主播[' + nickname + ']开播啦！今天的主题是：' + roomtitle \
           + '。直播间地址：http://live.bilibili.com/' + room
    ret = await dynamic.send_dynamic(text=text, credential=credential)
    dynamic_id = ret['dynamic_id']
    print('主播{}开播b站动态已发送'.format(nickname))


async def delete_dynamic(num):
    """
    下播删除开播b站动态
    """
    global dynamic_id
    room = config.items('RoomsStatus')[num][0]
    request = live.LiveRoom(eval(room))
    room_info = await request.get_room_info()
    nickname = room_info['anchor_info']['base_info']['uname']
    dynamicctl = dynamic.Dynamic(dynamic_id, credential)
    await dynamicctl.delete()
    print('主播{}开播b站动态已删除'.format(nickname))


def live_status(num, loop):
    """
    获取当前直播状态并执行动态操作
    """
    config.read(bilicfgpath)
    curstatus = eval(config.items('RoomsStatus')[num][1])
    if prestatus[num] == 0 and curstatus == 1:
        prestatus[num] = 1
        loop.run_until_complete(send_dynamic(num))
    elif prestatus[num] == 1 and curstatus == 0:
        prestatus[num] = 0
        loop.run_until_complete(delete_dynamic(num))


def control(loop, lock):
    """
    控制查询间隔
    同时查询多个房间的时间间隔应设置在30s以上
    """
    while True:
        lock.acquire()
        for num in range(len(config.items('RoomsStatus'))):
            live_status(num, loop)
        lock.release()
        time.sleep(30)


def run(loop, lock):
    print('b站动态模块启动')
    control(loop, lock)

# if __name__ == '__main__':
#     run()
