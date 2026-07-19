from dotenv import load_dotenv
from my_llm import MyLLM

load_dotenv()

# 实例化重写的客户端，并指定 provider
llm = MyLLM(provider='modelscope')

# llm_client = HelloAgentsLLM(
#     provider="ollama",
#     model="llama3", # 需与 `ollama run` 指定的模型一致
#     base_url="http://localhost:11434/v1",
#     api_key="ollama" # 本地服务同样不需要真实 Key
# )

# 准备消息
messages = [
    { "role": "user", "content": "你好，请介绍一下你自己" },
]

# 调用模型
response_stream = llm.invoke(messages)

# 打印响应
print("ModelScope Response:")
for chunk in response_stream:
    # chunk 在 my_llm 库中已经打印过一遍，这里只需要pass即可
    print(chunk, end="", flush=True)
    # pass 