**结论先行：**

* **协议流程不变**——FastMCP 完全实现 MCP 规范，所以仍旧是 *capabilities → resources/list → resources/read → （可选）subscribe*。
* **编写方式更“Pythonic”**——你几乎不用手写 JSON-RPC；FastMCP 给了统一的服务器装饰器和客户端 SDK 方法。
* **附加能力**：内建 async、资源/tag 筛选、`_meta._fastmcp` 扩展元数据、通配符模板、自动 list\_changed 通知等，比裸协议更省代码也更丰富。

---

## 1. FastMCP 客户端：一行拿到资源

```python
from fastmcp import AsyncClient   # pip install fastmcp>=2.0

async with AsyncClient("ws://localhost:4242") as client:
    # 列表
    resources = await client.list_resources()
    # 读取
    readme = await client.read_resource("file:///README.md")
    print(readme[0].text[:200])
```

* `list_resources()` / `read_resource()` / `list_resource_templates()` 都是 **SDK 包装**；实际仍发标准 JSON-RPC 请求，但你不需要自己拼报文。([gofastmcp.com][1])
* 想拿原始 JSON-RPC 结构，可用 `*_mcp()` 系列方法（例如 `list_resources_mcp()`）。([gofastmcp.com][1])
* 2.11+ 版本支持用 `_meta._fastmcp.tags` 做资源**标签过滤**：

  ````python
  cfg = [r for r in resources
         if 'config' in r._meta['_fastmcp']['tags']]
  ``` :contentReference[oaicite:2]{index=2}  
  ````

---

## 2. FastMCP 服务器：一个装饰器就暴露资源

```python
from fastmcp import FastMCP
mcp = FastMCP(name="DataServer")

# 静态/动态资源
@mcp.resource("resource://greeting")
def hello() -> str:
    """返回简单问候语"""
    return "Hello, FastMCP!"

# 带参数的资源模板
@mcp.resource("weather://{city}/current")
def weather(city: str) -> dict:
    return {"city": city, "temp": 28}

mcp.serve("0.0.0.0:4242")   # 内建 WebSocket JSON-RPC 服务
```

* 一个 `@mcp.resource(uri, …)` 就注册完资源；返回值会自动序列化为文本 / JSON / binary。([gofastmcp.com][2])
* 同一个函数可叠加多个模板 URI；支持 `{param}` 和 `{param*}` 通配符。([gofastmcp.com][2])
* 资源新增/禁用时，FastMCP 自动向客户端推送 `notifications/resources/list_changed`，省掉轮询。([gofastmcp.com][2])


---

### 小结

* **思维方式不换**：客户端仍按 *发现→列表→读取/订阅* 走。
* **代码行数大减**：一个装饰器 + 三个方法，剩下的交给 FastMCP。
* **功能多一些**：标签、通知、通配符、元数据、Async… 如果你只是想“先跑起来”，FastMCP 的默认实现基本开箱即用；后续再逐步切到更底层或自定义都没问题。

[1]: https://gofastmcp.com/clients/resources "Resource Operations - FastMCP"
[2]: https://gofastmcp.com/servers/resources "Resources & Templates - FastMCP"
