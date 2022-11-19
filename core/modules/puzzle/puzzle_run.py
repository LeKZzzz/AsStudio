# -*- coding: UTF-8 -*- 
# Creator：LeK
# Date：2022/11/14

import time
from scrapy.cmdline import execute
import json
import os
import random
from bilibili_api import Danmaku
import datetime
import sqlite3

my_prepath = os.path.join(os.path.dirname(__file__), 'puzzle', 'data', 'my')  # 谜语
score_prepath = os.path.join(os.path.dirname(__file__), 'puzzle', 'data', 'scores')  # 分数


def __create_cymy():  # 成语谜语
    execute(["scrapy", "crawl", "cymy_spider"])


def __create_zmmy():  # 字谜谜语
    execute(["scrapy", "crawl", "zmmy_spider"])


def __create_dwmy():  # 字谜谜语
    execute(["scrapy", "crawl", "dwmy_spider"])


def __create_dmmy():  # 灯谜谜语
    execute(["scrapy", "crawl", "dmmy_spider"])


def __check_data():
    """
    检查字谜文件是否完整
    :return:  None
    """
    cymy_filepath = os.path.join(my_prepath, "cymy.json")  # 成语谜语文件路径
    zmmy_filepath = os.path.join(my_prepath, "zmmy.json")  # 字谜谜语文件路径
    dwmy_filepath = os.path.join(my_prepath, "dwmy.json")  # 动物谜语文件路径
    dmmy_filepath = os.path.join(my_prepath, "dmmy.json")  # 灯谜谜语文件路径

    if not os.path.exists(cymy_filepath):
        __create_cymy()
    if not os.path.exists(zmmy_filepath):
        __create_zmmy()
    if not os.path.exists(dwmy_filepath):
        __create_dwmy()
    if not os.path.exists(dmmy_filepath):
        __create_dmmy()


def __read_json(filepath):
    """
    读取原有谜语块
    :param filepath:文件路径
    :return: 谜语字典
    """
    with open(filepath, 'r', encoding='utf8') as fp:
        data = json.load(fp)
        return data


def get_puzzle():
    """
    获取谜语
    :return:谜语字典
    """
    __check_data()  # 检查文件完整
    # 随机获取谜语
    filelist = os.listdir(my_prepath)
    curfile_index = random.randint(0, len(filelist) - 1)
    puzzle_file = __read_json(os.path.join(my_prepath, filelist[curfile_index]))
    curpuzzle_index = random.randint(0, puzzle_file['count'])
    return puzzle_file['data'][curpuzzle_index]


class puzzle_item:
    """
    谜语类
    """

    def __init__(self):
        self.mystery = None  # 谜面
        self.tips = None  # 提示
        self.answer = None  # 谜底
        self.pretime = datetime.datetime.now()  # 谜语的产生时间
        self.curtime = datetime.datetime.now()  # 当前时间
        self.premystery = None  # 上一个谜语的谜面
        self.pretips = None  # 上一个谜语的提示
        self.preanswer = None  # 上一个谜语的谜底

    def check_update(self):  # 检查是否需要更新谜语
        self.curtime = datetime.datetime.now()
        if abs((self.curtime - self.pretime).seconds) > 300:  # 时限5分钟
            return True
        else:
            return False

    def update(self, puzzle: dict):  # 更新谜语
        self.pretime = self.curtime
        self.premystery = self.mystery
        self.pretips = self.tips
        self.preanswer = self.answer
        self.mystery = Danmaku(text=puzzle['谜面'][0:20])
        self.tips = Danmaku(text=puzzle['提示'][0:20])
        self.answer = Danmaku(text=puzzle['谜底'][0:20])


def score_init():
    """
    分数数据库初始化
    :return: None
    """
    scores_filepath = os.path.join(score_prepath, "scores.db")
    if not os.path.exists(scores_filepath):
        conn = sqlite3.connect(scores_filepath)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE SCORES
                   (UID INT PRIMARY KEY     NOT NULL,
                   USERNAME           CHAR(50)    NOT NULL,
                   SCORE            INT     NOT NULL,
                   LAST_TIME        INT     NOT NULL);''')
        conn.commit()
        conn.close()
    pretime = int(time.time()) - (7 * 24 * 60 * 60)  # 过期时间，设置为7天
    conn = sqlite3.connect(scores_filepath)
    cur = conn.cursor()
    cur.execute("DELETE from SCORES where LAST_TIME<?;", (pretime,))  # 删除过期数据
    conn.commit()
    conn.close()


def score_update(uid: int, username: str):
    """
    分数更新
    :param uid:uid
    :param username:用户名
    :return: None
    """
    scores_filepath = os.path.join(score_prepath, "scores.db")
    conn = sqlite3.connect(scores_filepath)
    cur = conn.cursor()
    prescore = score_select(uid)
    if prescore == None:  # 记录不存在
        cur.execute(
            "INSERT INTO SCORES (UID,USERNAME,SCORE,LAST_TIME) VALUES (?,?,?,?)", (uid, username, 1, int(time.time())))
    else:  # 更新数据
        cur.execute("UPDATE SCORES set SCORE= ? where UID=?", (prescore + 1, uid))
        cur.execute("UPDATE SCORES set LAST_TIME= ? where UID=?", (int(time.time()), uid))
    conn.commit()
    conn.close()


def score_select(uid: int):
    """
    查找分数
    :param uid:uid
    :return: 分数或None
    """
    scores_filepath = os.path.join(score_prepath, "scores.db")
    conn = sqlite3.connect(scores_filepath)
    cur = conn.cursor()
    predata = cur.execute("SELECT UID,USERNAME,SCORE,LAST_TIME  from SCORES where UID =? ", (uid,))
    if predata == None:
        return None
    else:
        for row in predata:
            return row[2]