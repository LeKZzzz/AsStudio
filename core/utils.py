# -*- coding: UTF-8 -*- 
# Creator：LeK
# Date：2022/10/14
"""

通用工具库

"""

import os
import json


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
