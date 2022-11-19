# -*- coding: UTF-8 -*- 
# Creator：LeK
# Date：2022/10/26

from bilibili_api import live, Credential, Danmaku
import utils
import configparser
import json
import re
from modules.getweather import getweather
from modules.puzzle import puzzle_run
import time

# 配置文件读取
config = configparser.RawConfigParser()
bilicfgpath = utils.get_path('bili')
config.read(bilicfgpath, encoding='utf-8')
credential = Credential(sessdata=config['Cookie']['sessdata'],
                        bili_jct=config['Cookie']['bili_jct'],
                        buvid3=config['Cookie']['buvid3'])

# 日志对象
danmaku_logger = utils.Log("danmaku")  # 弹幕
gift_logger = utils.Log("gifts")  # 礼物
welcome_logger = utils.Log("welcome")  # 入场

# 直播管理对象
room_id = eval(config.items('RoomsStatus')[0][0])  # 房间id
live_danmaku = live.LiveDanmaku(room_display_id=room_id, credential=credential)  # 弹幕管理对象
live_room = live.LiveRoom(room_display_id=room_id, credential=credential)  # 直播间管理对象

# 谜语模块
puzzle = puzzle_run.puzzle_item()  # 谜语对象
puzzle_run.score_init()  # 初始化分数数据库，清理过期数据
key_pattern = '^#[\u4e00-\u9fa5]+\uff1a?:?[\u4e00-\u9fa5]+$'  # 触发词
mystery_pattern = '^#\u8c1c\u9762$'  # 谜面
tips_pattern = '^#\u63d0\u793a$'  # 提示
answer_pattern = '^#\u8c1c\u5e95(\uff1a|:)[\u4e00-\u9fa5]+$'  # 谜底
score_pattern = '^#\u5206\u6570$'  # 分数
change_pattern = '^#\u6362\u9898$'  # 换题


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
    identity = event['data']['info'][-1]
    print(username + ':', end=' ')
    print(msg)
    str = '[UID:{}] {}: {}'.format(uid, username, msg)
    danmaku_logger.info(str)

    # 模块功能
    function = json.loads(open(utils.get_path("function"), encoding="utf8").read())
    match = re.match(key_pattern, msg)
    if match:
        if function['getweather'] == True:  # 天气获取
            await get_weather(msg)

        if function['puzzle'] == True:  # 谜语游戏
            await puzzle_control(uid, username, msg, identity)


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
    thx_danmaku = Danmaku(text='感谢{}送的{}，老板糊涂！'.format(username, giftname))
    await live_room.send_danmaku(thx_danmaku)  # 发送感谢弹幕


@live_danmaku.on("WELCOME")  # 老爷进入房间
@live_danmaku.on("WELCOME_GUARD")  # 房管进入房间
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


# 功能模块

async def get_weather(msg: str):
    """
    天气获取
    :param msg:弹幕数据
    :return:None
    """
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


async def puzzle_control(uid: int, username: str, msg: str, identity: str):
    """
    猜谜游戏主控制函数
    :param uid:uid
    :param username:用户名
    :param msg: 弹幕数据
    :param identity: 弹幕发送者身份
    主播：210
    房管：91
    舰长：105
    :return:
    """
    flag = None  # 标记是否超时
    if puzzle.mystery == None:
        get_puzzle()
    right_danmaku = Danmaku(text='{}回答正确，进入下一题！'.format(username))  # 回答正确
    wrong_danmaku = Danmaku(text='{}回答错误！'.format(username))  # 回答错误
    if puzzle.check_update():  # 检查超时
        get_puzzle()
        flag = True

    if re.match(mystery_pattern, msg):  # 谜面弹幕
        if flag:
            await update_danmaku()
        await live_room.send_danmaku(puzzle.mystery)
    elif re.match(tips_pattern, msg):  # 提示弹幕
        if flag:
            await update_danmaku()
            await live_room.send_danmaku(puzzle.mystery)
        else:
            await live_room.send_danmaku(puzzle.tips)
    elif re.match(answer_pattern, msg):  # 谜底弹幕
        if flag:
            await update_danmaku()
            await live_room.send_danmaku(puzzle.mystery)
        else:
            user_answer = msg[4:]  # 弹幕回答
            print(user_answer)
            print(puzzle.answer.text[3:])
            if user_answer == puzzle.answer.text[3:]:
                await live_room.send_danmaku(right_danmaku)
                get_puzzle()  # 更新谜语
                puzzle_run.score_update(uid, username)  # 更新分数
                await live_room.send_danmaku(puzzle.mystery)
            else:
                await live_room.send_danmaku(wrong_danmaku)
    elif re.match(score_pattern, msg):  # 查分弹幕
        score = puzzle_run.score_select(uid)
        if score != None:
            score_danmaku = Danmaku(text='{}当前分数为{}分'.format(username, score))
        else:
            score_danmaku = Danmaku(text='{}当前分数为{}分'.format(username, 0))
        await live_room.send_danmaku(score_danmaku)
    elif re.match(change_pattern, msg):  # 换题弹幕
        if identity in (91, 105, 210):  # 主播、房管、舰长
            change_danmaku = Danmaku(text='{}更换了题目！'.format(username))
            await live_room.send_danmaku(change_danmaku)
            get_puzzle()


def get_puzzle():
    """
    更新谜语
    :return: None
    """
    puzzle_item = puzzle_run.get_puzzle()
    while len(puzzle_item['谜面']) > 20 or len(puzzle_item['提示']) > 20:
        puzzle_item = puzzle_run.get_puzzle()
    puzzle.update(puzzle_item)


async def update_danmaku():
    """
    谜语超时操作
    :return:
    """
    update_danmaku = Danmaku(text='上一个谜语时限已到，谜语更新！')  # 谜语更新
    last_danmaku = Danmaku(text='上一题答案为：{}'.format(puzzle.preanswer.text[3:]))  # 上一题答案
    await live_room.send_danmaku(last_danmaku)
    time.sleep(2)
    await live_room.send_danmaku(update_danmaku)
    time.sleep(2)


def run(loop):
    """
    运行danmaku模块
    :param loop: 事件循环
    :return: None
    """
    loop.run_until_complete(live_danmaku.connect())
