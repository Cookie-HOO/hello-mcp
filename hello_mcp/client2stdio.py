"""
Client for stdio mode MCP server
Reference implementation: https://modelcontextprotocol.io/quickstart/client
"""


import argparse
import asyncio
import json
from contextlib import AsyncExitStack
from typing import Optional, Dict, List

from mcp import StdioServerParameters, stdio_client, ClientSession

from hello_mcp.client import MCPClient


class MCPClient2SSE(MCPClient):
    def __init__(self, config_path: Optional[str] = None):
        super().__init__(config_path)

        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.stdio, self.write = None, None

    async def register_server(self, server_url_or_path: str) -> bool:
        """
        Register MCP server

        Args:
            server_url_or_path: Server URL or path

        Returns:
            Whether registration succeeded
        """
        try:
            is_python = server_url_or_path.endswith('.py')
            is_js = server_url_or_path.endswith('.js')
            if not (is_python or is_js):
                raise ValueError("Server script must be a .py or .js file")

            command = "python" if is_python else "node"
            server_params = StdioServerParameters(
                command=command,
                args=[server_url_or_path],
                env=None
            )

            stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
            self.stdio, self.write = stdio_transport
            self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

            await self.session.initialize()

            # List available tools
            # response = await self.session.list_tools()
            # tools = response.tools
            # print("\nConnected to server with tools:", [tool.name for tool in tools])
            return True
        except Exception as e:
            print(f"Failed to register server: {e}")
            return False

    async def get_available_tools(self) -> List[Dict]:
        """
        Get list of available tools from server

        Returns:
            List of tools
        """
        try:
            response = await self.session.list_tools()
            tools = response.tools
            return [{"name": tool.name, "description": tool.description, "parameters": tool.inputSchema} for tool in tools]
        except Exception as e:
            print(f"Failed to get tools list: {e}")
            return []

    async def call_tool(self, tool_name: str, arguments: Dict) -> Dict:
        try:
            result = await self.session.call_tool(tool_name, arguments)
            """[TextContent(type='text', text='{"type": "directory", "path": "/Users/bytedance/Desktop", "contents": [{"name": "~$mbti_famous_people.xlsx", "type": "file"}, {"name": "trump_tariff_analysis.md", "type": "file"}, {"name": ".DS_Store", "type": "file"}, {"name": ".localized", "type": "file"}, {"name": "\\u4eca\\u65e5\\u65b0\\u95fb\\u603b\\u7ed3.txt", "type": "file"}, {"name": "mbti_famous_people.xlsx", "type": "file"}, {"name": "mbti_famous_people.py", "type": "file"}]}', annotations=None)]"""
            return json.loads(result.content[0].text)
        except Exception as e:
            return {"error": f"Tool call failed: {str(e)}"}


async def main():
    """Command line entry point"""
    parser = argparse.ArgumentParser(description="MCP Client")
    parser.add_argument("--config", "-c", help="Path to config file")
    parser.add_argument("--server-path", "-s", help="Path to MCP server script")

    args = parser.parse_args()

    client = MCPClient2SSE(args.config)

    if args.server_path:
        await client.register_server(args.server_path)

    await client.chat()



if __name__ == "__main__":
    asyncio.run(main())
