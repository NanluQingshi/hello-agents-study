'''
Author: NanluQingshi
Date: 2026-07-18 16:17:20
LastEditors: NanluQingshi
LastEditTime: 2026-07-18 16:52:59
Description: 自定义LLM客户端，用于与ModelScope模型交互
'''
import os

from openai import OpenAI
from typing import Optional

from hello_agents import HelloAgentsLLM

class MyLLM(HelloAgentsLLM):
    """
    一个自定义的 LLM 客户端，通过继承增加了对 ModelScope 的支持。
    """
    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        provider: Optional[str] = None,
        **kwargs
    ):
        # 检查 provider 是否是我们想处理的 ‘modelscope’
        if provider == 'modelscope':
            print("正在使用自定义的 ModelScope Provider")
            self.provider = provider
        
            # 解析 ModelScope 的凭证
            self.api_key = api_key or os.getenv("MODELSCOPE_API_KEY")
            self.base_url = base_url or "https://api-inference.modelscope.cn/v1/"

            # 验证凭证是否存在
            if not self.api_key:
                raise ValueError("ModelScope API key not found. Please set MODELSCOPE_API_KEY environment variable.")
            
            # 设置默认模型和其它参数
            self.model = model or os.getenv("LLM_MODEL_ID") or "Qwen/Qwen2.5-VL-72B-Instruct"
            self.temperature = kwargs.get("temperature", 0.7)
            self.max_tokens = kwargs.get("max_tokens")
            self.timeout = kwargs.get("timeout", 60)

            # 使用获取的参数创建 OpenAI 客户端实例  
            self._client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=self.timeout
            )
            
        else:
            # 如果不是 ModelScope，调用父类的初始化方法
            super().__init__(model, api_key, base_url, provider, **kwargs)
            
    