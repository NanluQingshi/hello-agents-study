from typing import Any

from my_tool import MyTool

class MyToolRegistry: 
    '''
    自定义工具注册器
    '''
    def __init__(self):
        self._tools: dict[str, MyTool] = {}
        self._functions: dict[str, dict[str, Any]] = {}
        

    def register_tool(self, tool: MyTool):
        '''
        注册工具
        '''
        if tool.name in self._tools:
            print(f"⚠️ 警告: 工具 {tool.name} 已注册，将覆盖旧工具")
        self._tools[tool.name] = tool
        print(f"✅ 工具 '{tool.name}' 已注册。")
    
    def registry_function(self, name: str, description: str, func: Callable[[str], str]):
        '''
        直接注册函数作为工具（简便方式）

        Args:
            name: 工具名称
            description: 工具描述
            func: 工具函数，接受字符串参数，返回字符串结果
        '''
        if name in self._functions:
            print(f"⚠️ 警告: 工具 {name} 已注册，将被覆盖")
        self._functions[name] = {
            "description": description,
            "func": func
        }
        print(f"✅ 工具 '{name}' 已注册。")
        