# -*- coding: UTF-8 -*- 
# Creator：LeK
# Date：2022/10/13


from bilibili_api import dynamic, Credential
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

# 开播动态id
dynamic_id = [-1 for _ in config.items('RoomsStatus')]

async def __send_dynamic(num):
    """
    开播发送开播b站动态
    """
    room_id = config.items('RoomsStatus')[num][0]
    room_info = await utils.get_room_info(eval(room_id))
    nickname = room_info['nickname']  # 主播昵称
    roomtitle = room_info['roomtitle']  # 直播间标题
    text = '哔哩哔哩开播小喇叭：主播[' + nickname + ']开播啦！今天的主题是：' + roomtitle \
           + '。直播间地址：http://live.bilibili.com/' + room_id  # 开播动态文本
    ret = await dynamic.send_dynamic(text=text, credential=credential)  # 获取开播动态id
    dynamic_id[num] = ret['dynamic_id']
    print('主播{}开播b站动态已发送'.format(nickname))


async def __delete_dynamic(num):
    """
    下播删除开播b站动态
    """
    room_id = config.items('RoomsStatus')[num][0]
    room_info = await utils.get_room_info(eval(room_id))  # 获取直播间信息
    nickname = room_info['nickname']  # 主播昵称
    if dynamic_id[num] != -1:
        dynamicctl = dynamic.Dynamic(dynamic_id[num], credential)
        await dynamicctl.delete()
        print('主播{}开播b站动态已删除'.format(nickname))
    else:  # 开播时未发送开播动态因此无法删除
        print('主播{}本次直播并未发送开播动态或中途关闭了本程序'.format(nickname))


def __live_status(num, loop):
    """
    获取当前直播状态并执行动态操作
    """
    offline = [0, 2]  # 下播的直播间状态
    config.read(bilicfgpath)
    curstatus = eval(config.items('RoomsStatus')[num][1])

    if prestatus[num] in offline and curstatus == 1:  # 开播
        prestatus[num] = curstatus
        loop.run_until_complete(__send_dynamic(num))
    elif prestatus[num] == 1 and curstatus in offline:  # 下播
        prestatus[num] = curstatus
        loop.run_until_complete(__delete_dynamic(num))


def __control(loop, lock):
    """
    控制查询间隔
    同时查询多个房间的时间间隔应设置在30s以上
    """
    while True:
        lock.acquire()  # 加锁

        for num in range(len(config.items('RoomsStatus'))):
            __live_status(num, loop)

        lock.release()  # 释放锁

        time.sleep(120)  # 控制时间间隔


def run(loop, lock):
    """
    :param loop:事件循环
    :param lock: 线程锁
    """
    print('b站动态模块启动')
    __control(loop, lock)
