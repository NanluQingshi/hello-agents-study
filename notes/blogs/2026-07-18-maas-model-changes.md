# MaaS 平台踩坑记：你记住的模型名，可能明天就没了

> 一个让新手（和老手）都抓狂的 400 错误，背后是 MaaS 的常态

---

## 故事的开始

前两天我在折腾 ModelScope 的 API，想试试用它的 Qwen 模型跑个对话。代码写好了，token 也配好了，结果一跑——

```
openai.BadRequestError: Error code: 400
{'error': {'message': 'Model id : Qwen/Qwen2.5-VL-72B-Instruct , has no provider supported'}}
```

嗯？"has no provider supported"？模型名明明是从官网复制的，怎么会不支持？

换一个模型试试：

```
openai.BadRequestError: Error code: 400
{'error': {'message': 'Model id : Qwen/Qwen3-Coder-480B-A35B-Instruct , has no provider supported'}}
```

还是不行。我开始怀疑人生了。

## 踩坑全过程

### 第一坑：Token 认证失败

最初报的是 `401 Authentication failed`——token 无效。

排查发现：ModelScope 的 API 需要**绑定阿里云账号**才能使用，而且必须在 **`modelscope.cn`（cn 域名）** 下操作，国际站域名下绑定不了。

**教训**：国内服务用 cn 域名，别跑错地方。

### 第二坑：模型名不对

token 搞定了，又报 `400 has no provider supported`。

我试了 `Qwen/Qwen2.5-VL-72B-Instruct`、`Qwen/Qwen3-Coder-480B-A35B-Instruct`，都是官网存在的模型名，为什么 API 说"不支持"？

### 查到了真相

ModelScope 的 API 推理服务（`api-inference.modelscope.cn`）**只提供一部分模型的在线推理**，不是所有 ModelScope 上托管的模型都能通过 API 调用。

而且——**可用模型列表是会变的**。

```bash
# 用这个命令查当前可用的模型
curl -s "https://api-inference.modelscope.cn/v1/models" \
  -H "Authorization: Bearer 你的Token"
```

结果发现，我试的两个模型都不在列表里，但 `Qwen/Qwen3-Coder-30B-A3B-Instruct` 在。换上去，一次通过。

---

## 这不是 ModelScope 的问题，这是 MaaS 的常态

**MaaS（Model as a Service）** 平台上的可用模型**不是固定的**。原因很多：

| 原因 | 说明 |
|------|------|
| 模型下架 | 旧模型停止服务，被新版本替代 |
| 模型上新 | 新模型发布后才会加入 API |
| 服务商切换 | 模型由不同提供商托管，端点可能不同 |
| 账号权限 | 有些模型需要付费或特定权限才能用 |
| 地域差异 | 同一平台不同区域可用模型可能不同 |

这不是 ModelScope 独有的，所有 MaaS 平台都一样。你今天记住的模型名，明天可能就不在了。

---

## 正确做法：用之前先查

### 通用方案

不管用哪个平台，不要靠记忆写模型名。**用之前先调 API 查一下可用列表**：

| 平台 | 查询 API |
|------|----------|
| ModelScope | `GET /v1/models` |
| OpenAI | `GET /v1/models` |
| 阿里云百炼 | 官网文档 / 控制台 |
| DeepSeek | 官网文档 |

### 最佳实践

```python
import os
import requests
from openai import OpenAI

# 1. 先查可用模型
def get_available_models(base_url, api_key):
    response = requests.get(
        f"{base_url.rstrip('/')}/models",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    return [m["id"] for m in response.json().get("data", [])]

# 2. 选一个可用的
models = get_available_models(
    "https://api-inference.modelscope.cn/v1",
    os.getenv("MODELSCOPE_API_KEY")
)
print(f"可用模型 ({len(models)}):")
for m in models:
    print(f"  - {m}")

# 3. 再调用
client = OpenAI(
    base_url="https://api-inference.modelscope.cn/v1",
    api_key=os.getenv("MODELSCOPE_API_KEY")
)
```

---

## 附：当时可用的 Qwen 模型（2026-07-18）

```
Qwen/Qwen3-14B
Qwen/Qwen3-235B-A22B
Qwen/Qwen3-235B-A22B-Instruct-2507
Qwen/Qwen3-235B-A22B-Thinking-2507
Qwen/Qwen3-30B-A3B
Qwen/Qwen3-30B-A3B-Thinking-2507
Qwen/Qwen3-32B
Qwen/Qwen3-4B
Qwen/Qwen3-8B
Qwen/Qwen3-Coder-30B-A3B-Instruct
Qwen/Qwen3-Next-80B-A3B-Instruct
Qwen/Qwen3-Next-80B-A3B-Thinking
Qwen/Qwen3-VL-235B-A22B-Instruct
Qwen/Qwen3-VL-8B-Instruct
Qwen/Qwen3-VL-8B-Thinking
Qwen/Qwen3.5-122B-A10B
Qwen/Qwen3.5-27B
Qwen/Qwen3.5-35B-A3B
Qwen/Qwen3.5-397B-A17B
```

> ⚠️ 注意：这份列表是**快照**，到你读这篇文章时可能已经变了。用前记得查 API。

---

## 总结

| 建议 | 原因 |
|------|------|
| **API 查模型，别靠记忆** | 模型列表随时会变 |
| **用 cn 域名访问国内服务** | 国际站可能无法绑定账号 |
| **先查后调，失败有兜底** | 400 错误最常见的坑就是模型名不对 |
| **MaaS 不是 SaaS** | 模型即服务，意味着模型本身是动态的 |

**一句话：** MaaS 平台上的模型是"活"的，别把它当死数据。用之前查一下 API，省去半小时 debug。