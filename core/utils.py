# -*- coding: UTF-8 -*- 
# Creator：LeK
# Date：2022/10/14
"""

通用工具库

"""

import os
import json
from bilibili_api import live


def get_path(field: str):
    """
    获取配置文件路径

    Args:
        需要获取的配置文件

    Returns:
        配置文件路径
    """
    pathindex = os.path.join(os.path.dirname(__file__), "confpath.json")
    if os.path.exists(pathindex):
        with open(pathindex, encoding="utf8") as f:
            return os.path.join(os.path.dirname(__file__), '..', json.loads(f.read())[field])


async def get_room_info(room_id):
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
