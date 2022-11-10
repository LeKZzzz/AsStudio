# -*- coding: UTF-8 -*- 
# Creator：LeK
# Date：2022/11/9


import requests
import time
import re
import requests.packages.urllib3.util.connection as urllib3_cn
from urllib import parse
from bs4 import BeautifulSoup

# 强制使用IPv4协议
# def allowed_gai_family():
#     family = socket.AF_INET
#     return family
# urllib3_cn.allowed_gai_family = allowed_gai_family

urllib3_cn.HAS_IPV6 = False


def get_number(site: str):
    """
    获取地点编号
    :param site:地点名
    :return: 地点编号
    """
    url_encode = parse.quote(site)  # 地点的url编码
    url = 'http://weather.cma.cn/api/autocomplete?q={}&limit=10&timestamp={}'.format(url_encode, int(time.time()))
    response = requests.get(url)
    pattern = "([0-9]+)\|([\u4e00-\u9fa5]+)\|([A-Za-z]+|[\u4e00-\u9fa5]+)\|([\u4e00-\u9fa5]+)"
    result = re.findall(pattern, response.text)
    for item in result:
        if item[1] == site:
            return item[0]
    else:
        return None


def get_weather(site: str):
    """
    获取地点天气
    :param site:地点名
    :return: 地点名、天气、气温
    """
    number = get_number(site)
    if number == None:
        return None
    url = 'http://weather.cma.cn/web/weather/{}.html'.format(number)
    response = requests.get(url)
    unpack = BeautifulSoup(response.content, features='lxml')
    day_item = unpack.find_all('div', class_="day-item", limit=10)
    item_transform = []
    for item in day_item:
        item_transform.append(item.get_text().strip())
    temperature = re.findall('(-?[0-9]+)\u2103', item_transform[5])
    weather_begin = item_transform[2]
    weather_end = item_transform[7]
    result = {}
    result['site'] = site
    result['high_temperature'] = temperature[0]
    result['low_temperature'] = temperature[1]
    result['weather_begin'] = weather_begin
    result['weather_end'] = weather_end
    return result


def run(danmaku: str):
    """
    运行模块
    :param danmaku:弹幕
    :return: 地点名、天气、气温
    """
    pattern = '^#[\u4e00-\u9fa5]+\u5929\u6c14$'
    match = re.match(pattern, danmaku)
    if match:
        if match.string[-3] == '市':
            return get_weather(match.string[1:-3])
        else:
            return get_weather(match.string[1:-2])
    else:
        return None
