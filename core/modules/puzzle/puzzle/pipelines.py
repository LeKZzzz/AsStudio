# -*- coding: UTF-8 -*-
# Creator：LeK
# Date：2022/11/14

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import os


class CymyPipeline:  # 成语谜语
    def process_item(self, item, spider):
        if spider.name == 'cymy_spider':
            items = []
            mystery = item['mystery']
            answer = item['answer']
            if item['tips'] == None:
                tips = "小贴士：无"
            else:
                tips = item['tips']

            add_item = {"谜面": mystery,  # 谜语块
                        "提示": tips,
                        "谜底": answer}

            filepath = os.path.join(os.path.dirname(__file__), 'data', 'my', "cymy.json")  # 文件路径

            if not os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf8') as fp:
                    items.append(add_item)
                    data = {"data": items, "count": 1}
                    json.dump(data, fp, ensure_ascii=False, indent=4)
            else:
                pre_data = self.read_json(filepath)
                items = pre_data['data']
                items.append(add_item)
                new_count = pre_data['count'] + 1
                new_data = {"data": items, "count": new_count}
                with open(filepath, 'w', encoding='utf8') as fp:
                    json.dump(new_data, fp, ensure_ascii=False, indent=4)
        return item

    def read_json(self, filepath):  # 读取原有谜语块
        with open(filepath, 'r', encoding='utf8') as fp:
            data = json.load(fp)
            return data


class ZmmyPipeline:  # 字谜谜语
    def process_item(self, item, spider):
        if spider.name == 'zmmy_spider':
            items = []
            mystery = item['mystery']
            answer = item['answer']
            tips = item['tips']

            add_item = {"谜面": mystery,  # 谜语块
                        "提示": tips,
                        "谜底": answer}

            filepath = os.path.join(os.path.dirname(__file__), 'data', 'my', "zmmy.json")  # 文件路径

            if not os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf8') as fp:
                    items.append(add_item)
                    data = {"data": items, "count": 1}
                    json.dump(data, fp, ensure_ascii=False, indent=4)
            else:
                pre_data = self.read_json(filepath)
                items = pre_data['data']
                items.append(add_item)
                new_count = pre_data['count'] + 1
                new_data = {"data": items, "count": new_count}
                with open(filepath, 'w', encoding='utf8') as fp:
                    json.dump(new_data, fp, ensure_ascii=False, indent=4)
        return item

    def read_json(self, filepath):  # 读取原有谜语块
        with open(filepath, 'r', encoding='utf8') as fp:
            data = json.load(fp)
            return data


class DwmyPipeline:  # 动物谜语
    def process_item(self, item, spider):
        if spider.name == 'dwmy_spider':
            items = []
            mystery = item['mystery']
            answer = item['answer']
            tips = item['tips']

            add_item = {"谜面": mystery,  # 谜语块
                        "提示": tips,
                        "谜底": answer}

            filepath = os.path.join(os.path.dirname(__file__), 'data', 'my', "dwmy.json")  # 文件路径

            if not os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf8') as fp:
                    items.append(add_item)
                    data = {"data": items, "count": 1}
                    json.dump(data, fp, ensure_ascii=False, indent=4)
            else:
                pre_data = self.read_json(filepath)
                items = pre_data['data']
                items.append(add_item)
                new_count = pre_data['count'] + 1
                new_data = {"data": items, "count": new_count}
                with open(filepath, 'w', encoding='utf8') as fp:
                    json.dump(new_data, fp, ensure_ascii=False, indent=4)
        return item

    def read_json(self, filepath):  # 读取原有谜语块
        with open(filepath, 'r', encoding='utf8') as fp:
            data = json.load(fp)
            return data

class DmmyPipeline:  # 灯谜谜语
    def process_item(self, item, spider):
        if spider.name == 'dmmy_spider':
            items = []
            mystery = item['mystery']
            answer = item['answer']
            tips = item['tips']

            add_item = {"谜面": mystery,  # 谜语块
                        "提示": tips,
                        "谜底": answer}

            filepath = os.path.join(os.path.dirname(__file__), 'data', 'my', "dmmy.json")  # 文件路径

            if not os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf8') as fp:
                    items.append(add_item)
                    data = {"data": items, "count": 1}
                    json.dump(data, fp, ensure_ascii=False, indent=4)
            else:
                pre_data = self.read_json(filepath)
                items = pre_data['data']
                items.append(add_item)
                new_count = pre_data['count'] + 1
                new_data = {"data": items, "count": new_count}
                with open(filepath, 'w', encoding='utf8') as fp:
                    json.dump(new_data, fp, ensure_ascii=False, indent=4)
        return item

    def read_json(self, filepath):  # 读取原有谜语块
        with open(filepath, 'r', encoding='utf8') as fp:
            data = json.load(fp)
            return data