# -*- coding: UTF-8 -*- 
# Creator：LeK
# Date：2022/10/14
"""

更新受监控直播间的当前状态

"""

from bilibili_api import live
import utils
import configparser
import asyncio
import time

# 配置文件读取
config = configparser.RawConfigParser()
bilicfgpath = utils.get_path('bili')
config.read(bilicfgpath, encoding='utf-8')

# 直播间上一次查询时的状态
prestatus = [eval(status[1]) for status in config.items('RoomsStatus')]


async def __update(num):
    """
    获取当前直播状态并进行更新
    """
    room = config.items('RoomsStatus')[num][0]
    request = live.LiveRoom(eval(room))
    result = await request.get_room_play_info()
    curstatus = result['live_status']
    config.set('RoomsStatus', room, curstatus)
    config.write(open(bilicfgpath, 'w'))

    if prestatus[num] == 0 and curstatus == 1:
        print('{}已开播'.format(room))
        prestatus[num] = 1
    elif prestatus[num] == 1 and curstatus == 0:
        print('{}已下播'.format(room))
        prestatus[num] = 0
    elif prestatus[num] == 0 and curstatus == 0:
        print('{}未开播'.format(room))
    else:
        print('{}直播中'.format(room))


def __control(loop, lock):
    """
    控制查询间隔
    同时查询多个房间的时间间隔应设置在30s以上
    """
    while True:
        lock.acquire()

        print('===============当前轮次开始===============')
        checkingrooms = [__update(num) for num in range(len(config.items('RoomsStatus')))]
        loop.run_until_complete(asyncio.wait(checkingrooms))
        print('===============当前轮次结束===============')

        lock.release()

        time.sleep(30)


def run(loop, lock):
    print('状态更新模块启动')
    __control(loop, lock)


if __name__ == '__main__':
    run()
