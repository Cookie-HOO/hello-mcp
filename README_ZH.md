# Hello-MCP

一个非常简单的MCP（Model Control Protocol）客户端和服务器实现。
用以帮助理解 MCP 协议是什么

本项目可以✅：让你了解到MCP协议的本质，自己动手开发一个MCP Client 和 Server
本项目不行❌：教你配置现有的MCP Host，实现通用Server功能，需要自行探索

## 功能特点

### MCP客户端
- 支持注册 MCP Server（支持 SSE 和 stdio 两种方式注册）
- 命令行交互式聊天界面
- 支持 DeepSeek API 进行对话（通过配置文件设置DeepSeek API密钥）
- 流式输出响应

### MCP服务器
- 基于 FastMCP 实现的简单服务器（支持 SSE 和 stdio 两种方式提供）
- 提供一个简单的路径工具（列出指定路径的所有文件）
- 支持健康检查

## 示例
使用 List_Dir 工具，获取所有项目的文件，然后进行分析
![](demo.gif)


## 使用方式

### 环境准备

> 推荐使用uv进行项目管理

#### 0. 下载项目

```bash
git clone https://github.com/Cookie-HOO/hello-mcp.git
cd hello-mcp
```

#### 1. 安装 uv

[uv安装的官方文档](https://docs.astral.sh/uv/getting-started/installation/)

mac：命令行安装
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

win： 注意：需要 powershell 安装而不是普通命令行
```shell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
   
#### 2. 项目依赖初始化

```shell
uv venv  # 创建虚拟环境
uv sync  # 安装依赖
source ./.venv/bin/activate  # mac：激活虚拟环境
.\.venv\Scripts\activate     # win：激活虚拟环境
```

#### 3. 设置 DeepSeek 密钥
本项目目前仅支持 DeepSeek API，可在DeepSeek官方进行申请
[DeepSeek API开放平台](https://platform.deepseek.com/api_keys)

```bash
cp ./config.example.yaml ./config.yaml
# 修改你的 DeepSeek 密钥
```

#### 4. 启动项目

```bash
# 第一种方式：stdio（只需显式启动client）
python -m hello_mcp.client2stdio --server-path ./hello_mcp/server.py

# 第二种方式：sse（需要显式启动server 和 client）
python -m hello_mcp.server --transport sse  # sse的方式启动服务端
python -m hello_mcp.client2sse --server-url http://127.0.0.1:8000  # 将刚启动的 mcp server 注册到client中
```

### 调试 MCP Server
```bash
uv run mcp dev hello_mcp/server.py
```
![](MCP%20Inspector.png)

### 结果展示

## 许可证

本项目采用MIT许可证。详见[LICENSE](LICENSE)文件。 

👏 欢迎来提issue和讨论


## MCP 日常使用说明

### 1. 我如何在日常中使用 MCP
1. 找到一个支持MCP Server 的 Host
2. 配置 MCP Server

附：MCP 官方给的Host列表

| Client             | Resources | Prompts | Tools | Sampling | Roots | Notes                                   |
|--------------------|-----------|---------|-------|----------|-------|-----------------------------------------|
| 5ire               | ❌         | ❌       | ✅     | ❌        | ❌     | Supports tools.                         |
| Apify MCP Tester   | ❌         | ❌       | ✅     | ❌        | ❌     | Supports tools                          |
| BeeAI Framework    | ❌         | ❌       | ✅     | ❌        | ❌     | Supports tools in agentic workflows.    |
| Claude Code        | ❌         | ✅       | ✅     | ❌        | ❌     | Supports prompts and tools              |
| Claude Desktop App | ✅         | ✅       | ✅     | ❌        | ❌     | Supports tools, prompts, and resources. |
| Cline              | ✅         | ❌       | ✅     | ❌        | ❌     | Supports tools and resources.           |
| Continue           | ✅         | ✅       | ✅     | ❌        | ❌     | Supports tools, prompts, and resources. |
| Copilot-MCP        | ✅         | ❌       | ✅     | ❌        | ❌     | Supports tools and resources.           |
| Cursor             | ❌         | ❌       | ✅     | ❌        | ❌     | Supports tools.                         |


### 2. 我怎么找 MCP 工具

| 资源                                                                        | 推荐          |
| ------------------------------------------------------------------------- |-------------|
| [Smithery - Model Context Protocol Registry](https://smithery.ai/)        | 🌟🌟🌟          |
| https://github.com/punkpeye/awesome-mcp-servers                           |   🌟🌟🌟         |
| https://github.com/modelcontextprotocol/servers                           |   🌟🌟🌟         |
| [List of all MCP Servers (42) \| Portkey](https://portkey.ai/mcp-servers) | 🌟🌟    |
| https://cursor.directory/mcp                                              |    🌟🌟        |
| [Open-Source MCP servers \| Glama](https://glama.ai/mcp/servers)          | 🌟🌟 |
| https://mcp.so/                                                           |     🌟🌟        |
| https://www.pulsemcp.com/servers                                          |    🌟🌟         |
| [Awesome MCP Servers](https://mcpservers.org/)                            |    🌟🌟         |


## 关于 MCP 概念的 Q & A

### Q：MCP为了解决什么问题
A：MCP(Model Control Protocol)主要解决以下问题：
1. 标准化AI模型与外部系统的交互协议
2. 提供统一的工具调用规范
3. 简化复杂AI系统的集成
4. 实现模型能力的模块化和复用

### Q：MCP的历史
A：MCP的发展历程：
1. 2023年：由Anthropic首次提出概念（Claude的母公司）
2. 2024年：多个开源实现出现
3. 2025年：成为AI系统集成的标准协议之一
4. 目前：被广泛应用于各类AI代理系统

### Q：MCP的现状
A：当前MCP的主要应用场景：
1. AI助手系统
2. 自动化工作流
3. 多模型协作平台
4. 企业级AI解决方案
主流实现包括FastMCP、PyMCP等

---

### Q：MCP 和 Function Call 的异同
A：相同点：
1. 都是执行特定功能的方式
2. 都需要定义输入输出
不同点：
1. MCP是标准化协议，Function Call是编程语言特性
2. MCP支持跨语言/跨平台调用
3. MCP包含完整的工具发现和注册机制

### Q: MCP 和 Agent的异同
A：关系说明：
1. Agent是使用MCP的主体
2. MCP是Agent之间或Agent与工具交互的协议
3. 一个Agent可以注册多个MCP工具

## 项目相关 Q & A
### Q：如何解决DeepSeek API密钥配置问题？
A：确保config.yaml文件中的api_key字段已正确填写，并且没有多余的空格或引号。如果遇到认证问题，可以尝试重新生成API密钥。

### Q：启动服务时报端口占用错误怎么办？
A：可以尝试以下方法：
1. 使用`lsof -i :8000`查看占用进程
2. 终止占用进程或修改server启动端口
3. 修改client注册的服务器地址

### Q：如何扩展新的MCP工具？
A：可以通过以下步骤：
1. 在server.py中添加新的工具函数
2. 使用@tool装饰器注册工具
3. 定义输入参数schema
4. 在client中测试调用

### Q：uv sync命令失败怎么办？
A：可能原因及解决方案：
1. 网络问题 - 检查网络连接
2. 依赖冲突 - 尝试删除.venv后重新创建
3. 权限问题 - 使用sudo或修改目录权限

### Q：如何贡献代码？
A：欢迎通过GitHub提交PR：
1. Fork本项目
2. 创建新分支开发
3. 提交清晰的commit信息
4. 创建Pull Request
