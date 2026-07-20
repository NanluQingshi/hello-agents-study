'''
Author: NanluQingshi
Date: 2026-07-20 00:05:30
LastEditors: NanluQingshi
LastEditTime: 2026-07-20 00:07:39
Description: 自定义工具类
'''

from typing import Dict, Any, List
from abc import ABC, abstractmethod
from my_tool_parameter import MyToolParameter

class MyTool(ABC):
    '''
    工具基类
    '''
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def run(self, parameters: Dict[str, Any]) -> str:
        '''
        工具执行方法
        '''
        pass
    
    @abstractmethod
    def get_parameters(self) -> List[MyToolParameter]:
        '''
        获取工具参数
        '''
        pass