'''
Author: NanluQingshi
Date: 2026-07-20 00:07:48
LastEditors: NanluQingshi
LastEditTime: 2026-07-20 00:10:13
Description: 自定义工具参数类
'''
from typing import Any
from pydantic import BaseModel

class MyToolParameter(BaseModel):
    '''
    工具参数类
    '''
    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None