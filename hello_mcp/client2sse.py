"""
SSE mode MCP client

register_server:      Checks /health endpoint availability
get_available_tools:  Gets all tools via /tools endpoint
call_tool:            Calls tools via /tools/{name} endpoint
"""


import argparse
import asyncio
from typing import Dict, List, Optional

import httpx

from hello_mcp.client import MCPClient


class MCPClient2SSE(MCPClient):
    def __init__(self, config_path: Optional[str] = None):
        super().__init__(config_path)
        self.server_url = None

    def register_server(self, server_url_or_path: str) -> bool:
        """
        Register MCP server

        Args:
            server_url_or_path: Server URL or address

        Returns:
            Whether registration succeeded
        """
        try:
            response = httpx.get(f"{server_url_or_path}/health")
            if response.status_code == 200:
                # Update configuration
                self.server_url = server_url_or_path

                print(f"Successfully registered MCP server: {server_url_or_path}")
                return True
            else:
                print(f"Server connection failed, status code: {response.status_code}")
                return False
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
            response = httpx.get(f"{self.server_url}/tools")
            if response.status_code == 200:
                tools = response.json()
                return tools
            else:
                print(f"Failed to get tools list, status code: {response.status_code}")
                return []
        except Exception as e:
            print(f"Failed to get tools list: {e}")
            return []

    async def call_tool(self, tool_name: str, arguments: Dict) -> Dict:
        try:
            response = httpx.post(
                f"{self.server_url}/tools/{tool_name}",
                json=arguments,
                timeout=30.0
            )

            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Tool call failed, status code: {response.status_code}"}
        except Exception as e:
            return {"error": f"Tool call error: {str(e)}"}


def main():
    """Command line entry point"""
    parser = argparse.ArgumentParser(description="MCP Client")
    parser.add_argument("--config", "-c", help="Path to config file")
    parser.add_argument("--server-url", "-s", help="MCP server URL to register")

    args = parser.parse_args()

    client = MCPClient2SSE(args.config)

    if args.server_url:
        client.register_server(args.server_url)

    asyncio.run(client.chat())


if __name__ == "__main__":
    main()
