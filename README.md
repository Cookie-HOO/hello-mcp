# Hello-MCP 🚀

---
[中文文档](README_ZH.md) 🇨🇳

A simple implementation of MCP (Model Control Protocol) client and server.
Helps understand what MCP protocol is and how it works.

This project will ✅:
- Teach you the essence of MCP protocol
- Let you build your own MCP Client and Server
- Provide hands-on experience with MCP implementation

This project won't ❌:
- Teach you how to configure existing MCP Hosts
- Implement generic server functionality (requires your own exploration)

## Features ✨

### MCP Client
- Supports registering MCP Server (both SSE and stdio methods)
- Interactive command line chat interface
- Supports DeepSeek API conversations (configure API key in config file)
- Streamed response output

### MCP Server
- Simple server based on FastMCP (supports both SSE and stdio)
- Provides a basic path utility (lists all files in specified path)
- Health check support

## DEMO
Use List_Dir Tool to get files and analysis!
![](demo.gif)

## Usage Guide 📖

### Environment Setup

> Recommended to use uv for project management

#### 0. Clone the project

```bash
git clone https://github.com/Cookie-HOO/hello-mcp.git
cd hello-mcp
```

#### 1. Install uv

[Official uv installation docs](https://docs.astral.sh/uv/getting-started/installation/)

macOS:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (requires PowerShell):
```shell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 2. Initialize project dependencies

```shell
uv venv  # Create virtual environment
uv sync  # Install dependencies
source ./.venv/bin/activate  # macOS: activate virtual environment
.\.venv\Scripts\activate     # Windows: activate virtual environment
```

#### 3. Set up DeepSeek API key
Currently only supports DeepSeek API - apply at:
[DeepSeek API Platform](https://platform.deepseek.com/api_keys)

```bash
cp ./config.example.yaml ./config.yaml
# Edit to add your DeepSeek API key
```

#### 4. Run the project

```bash
# Method 1: stdio (only need to explicitly start client)
python -m hello_mcp.client2stdio --server-path ./hello_mcp/server.py

# Method 2: SSE (need to explicitly start both server and client)
python -m hello_mcp.server --transport sse  # Start server in SSE mode
python -m hello_mcp.client2sse --server-url http://127.0.0.1:8000  # Register the MCP server with client
```

### Debugging MCP Server
```bash
uv run mcp dev hello_mcp/server.py
```
![](MCP%20Inspector.png)

## License 📜

MIT License. See [LICENSE](LICENSE) file for details.

👋 Contributions welcome! Feel free to open issues and discussions.


## MCP Usage Guide 🛠️

### 1. How to use MCP in daily work
1. Find an MCP Server Host that supports your needs
2. Configure the MCP Server

MCP Host reference list:

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

### 2. How to find MCP tools

| Resource                                                                 | Recommendation |
| ------------------------------------------------------------------------- | ------------- |
| [Smithery - Model Context Protocol Registry](https://smithery.ai/)        | 🌟🌟🌟          |
| https://github.com/punkpeye/awesome-mcp-servers                           | 🌟🌟🌟         |
| https://github.com/modelcontextprotocol/servers                           | 🌟🌟🌟         |
| [List of all MCP Servers (42) \| Portkey](https://portkey.ai/mcp-servers) | 🌟🌟    |
| https://cursor.directory/mcp                                              | 🌟🌟        |
| [Open-Source MCP servers \| Glama](https://glama.ai/mcp/servers)          | 🌟🌟 |
| https://mcp.so/                                                           | 🌟🌟        |
| https://www.pulsemcp.com/servers                                          | 🌟🌟         |
| [Awesome MCP Servers](https://mcpservers.org/)                            | 🌟🌟         |

## MCP Concept Q&A ❓

### Q: What problems does MCP solve?
A: MCP (Model Control Protocol) addresses:
1. Standardizing AI model interaction protocols
2. Providing unified tool calling specifications  
3. Simplifying complex AI system integration
4. Enabling modular and reusable model capabilities

### Q: History of MCP
A: MCP development timeline:
1. 2023: Concept introduced by Anthropic (Claude's parent company)
2. 2024: Multiple open-source implementations emerged
3. 2025: Became a standard protocol for AI system integration
4. Present: Widely used in various AI agent systems

### Q: Current state of MCP
A: Main application scenarios:
1. AI assistant systems
2. Automated workflows  
3. Multi-model collaboration platforms
4. Enterprise AI solutions
Popular implementations include FastMCP, PyMCP etc.

---

### Q: Differences between MCP and Function Call
A: Similarities:
1. Both execute specific functions
2. Both require input/output definitions
Differences:
1. MCP is a standardized protocol, Function Call is a language feature
2. MCP supports cross-language/platform calls
3. MCP includes complete tool discovery/registration

### Q: Relationship between MCP and Agents
A: Key points:
1. Agents are entities that use MCP
2. MCP is the protocol for Agent-Agent or Agent-Tool interaction  
3. One Agent can register multiple MCP tools

## Project Q&A 💡

### Q: How to solve DeepSeek API key configuration issues?
A: Ensure:
1. api_key field in config.yaml is correctly filled
2. No extra spaces or quotes in the key
3. Try regenerating API key if authentication fails

### Q: Port already in use when starting server?
A: Solutions:
1. Check processes using port with `lsof -i :8000`
2. Terminate process or change server port
3. Update client registration URL

### Q: How to extend with new MCP tools?
A: Steps:
1. Add new tool function in server.py
2. Register with @tool decorator  
3. Define input parameter schema
4. Test calling from client

### Q: uv sync command fails?
A: Possible solutions:
1. Check network connection
2. Delete .venv and recreate for dependency conflicts
3. Use sudo or fix directory permissions

### Q: How to contribute code?
A: Welcome PRs on GitHub:
1. Fork the project
2. Create feature branch
3. Commit with clear messages
4. Open Pull Request
