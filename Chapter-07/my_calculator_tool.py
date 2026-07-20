'''
Author: NanluQingshi
Date: 2026-07-20 13:39:07
LastEditors: NanluQingshi
LastEditTime: 2026-07-20 13:39:25
Description: 自定义计算器工具
'''
import ast
import operator
import math
from hello_agents import ToolRegistry


def my_calculator_tool(expression: str) -> str:
    """自定义计算器工具"""
    if not expression.strip():
        return "请输入要计算的表达式"

    # 支持的计算类型
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }
    # 支持的基本函数
    functions = {
        'sqrt': math.sqrt,
        'pi': math.pi,
    }
    try:
        node = ast.parse(expression)
        result = _eval_node(node.body, operators, functions)
        return str(result)
    except Exception as e:
        return f"计算错误: {str(e)}"

def _eval_node(node, operators, functions):
    """简化的表达式求值"""
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.BinOp):
        left = _eval_node(node.left, operators, functions)
        right = _eval_node(node.right, operators, functions)
        op = operators.get(type(node.op))
        return op(left, right)
    elif isinstance(node, ast.Call):
        func_name = node.func.id
        if func_name in functions:
            args = [_eval_node(arg, operators, functions) for arg in node.args]
            return functions[func_name](*args)
    elif isinstance(node, ast.Name):
        if node.id in functions:
            return functions[node.id]

def create_calculator_registry():
    """创建包含计算器的工具注册表"""
    registry = ToolRegistry()

    # 注册计算器函数
    registry.register_function(
        name="my_calculator",
        description="简单的数学计算工具，支持基本运算(+,-,*,/)和sqrt函数",
        func=my_calculate
    )

    return registry