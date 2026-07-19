'''
Author: NanluQingshi
Date: 2026-07-19 23:41:02
LastEditors: NanluQingshi
LastEditTime: 2026-07-19 23:50:03
Description: 反思Agent
'''

from typing import Optional, Dict
from hello_agents import ReflectionAgent, HelloAgentsLLM, Config


DEFAULT_PROMPTS = {
    "initial": """
    请根据以下要求完成任务:

    任务: {task}

    请提供一个完整、准确的回答。
    """,
        "reflect": """
    请仔细审查以下回答，并找出可能的问题或改进空间:

    # 原始任务:
    {task}

    # 当前回答:
    {content}

    请分析这个回答的质量，指出不足之处，并提出具体的改进建议。
    如果回答已经很好，请回答"无需改进"。
    """,
        "refine": """
    请根据反馈意见改进你的回答:

    # 原始任务:
    {task}

    # 上一轮回答:
    {last_attempt}

    # 反馈意见:
    {feedback}

    请提供一个改进后的回答。
"""
}

class MyReflectionAgent(ReflectionAgent):
    """
    反思Agent
    """
    def __init__(self, name: str, llm: HelloAgentsLLM, system_prompt: Optional[str] = None, config: Optional[Config] = None, max_iterations: int = 3, custom_prompts: Optional[Dict[str, str]] = None):
        super().__init__(name, llm, system_prompt, config, max_iterations, custom_prompts)
        self.prompt_template = custom_prompts if custom_prompts else DEFAULT_PROMPTS
        print(f"✅ {self.name} 初始化完成")