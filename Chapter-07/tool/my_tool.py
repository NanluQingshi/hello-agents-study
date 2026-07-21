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
    
    def get_tools_description(self) -> str:
        """获取所有可用工具的格式化描述字符串"""
        descriptions = []
        
        # MyTool 对象描述
        for tool in self._tools.values():
            descriptions.append(f"- {tool.name}: {tool.description}")
            
        # 函数工具描述
        for name, info in self._functions.items():
            descriptions.append(f"- {name}: {info['description']}")
            
        return "\n".join(descriptions) if descriptions else "暂无可用工具"

    def to_openai_schema(self) -> Dict[str, Any]:
        """转换为 OpenAI function calling schema 格式

        用于 FunctionCallAgent，使工具能够被 OpenAI 原生 function calling 使用

        Returns:
            符合 OpenAI function calling 标准的 schema
        """
        parameters = self.get_parameters()

        # 构建 properties
        properties = {}
        required = []

        for param in parameters:
            # 基础属性定义
            prop = {
                "type": param.type,
                "description": param.description
            }

            # 如果有默认值，添加到描述中（OpenAI schema 不支持 default 字段）
            if param.default is not None:
                prop["description"] = f"{param.description} (默认: {param.default})"

            # 如果是数组类型，添加 items 定义
            if param.type == "array":
                prop["items"] = {"type": "string"}  # 默认字符串数组

            properties[param.name] = prop

            # 收集必需参数
            if param.required:
                required.append(param.name)

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }
