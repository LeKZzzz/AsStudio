# -*- coding: UTF-8 -*- 
# Creator：LeK
# Date：2022/10/14
"""

更新受监控直播间的直播状态

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

# 日志对象
logger = utils.Log("status")


async def __update(num):
    """
    获取当前直播状态并进行更新
    """
    offline = [0, 2]  # 下播的直播间状态
    room_id = config.items('RoomsStatus')[num][0]
    request = live.LiveRoom(eval(room_id))
    result = await request.get_room_play_info()  # 查询直播间状态
    curstatus = result['live_status']
    config.set('RoomsStatus', room_id, curstatus)  # 写入直播间状态
    config.write(open(bilicfgpath, 'w'))

    if prestatus[num] in offline and curstatus == 1:  # 开播
        logger.info('{}已开播'.format(room_id))
        print('{}已开播'.format(room_id))
        prestatus[num] = curstatus
    elif prestatus[num] == 1 and curstatus in offline:  # 下播
        logger.info('{}已下播'.format(room_id))
        print('{}已下播'.format(room_id))
        prestatus[num] = curstatus
    elif prestatus[num] in offline and curstatus in offline:  # 未开播
        logger.info('{}未开播'.format(room_id))
        print('{}未开播'.format(room_id))
    else:
        logger.info('{}直播中'.format(room_id))
        print('{}直播中'.format(room_id))  # 直播中


def __control(loop, lock):
    """
    控制查询间隔
    同时查询多个房间的时间间隔应设置在30s以上
    """
    while True:
        lock.acquire()  # 加锁

        checkingrooms = [__update(num) for num in range(len(config.items('RoomsStatus')))]
        loop.run_until_complete(asyncio.wait(checkingrooms))
        logger.info('===============当前轮次结束===============')
        print('===============当前轮次结束===============')
        lock.release()  # 释放锁

        time.sleep(120)  # 控制时间间隔


def run(loop, lock):
    """
    :param loop:事件循环
    :param lock: 线程锁
    """
    logger.info('状态更新模块启动')
    logger.info('========================================')
    print('状态更新模块启动')
    print('========================================')
    __control(loop, lock)
