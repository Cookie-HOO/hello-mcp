"""
Base MCP client class with two implementations:
    ./client2sse.py:     Connect to MCP server in SSE mode
    ./client2stdio.py:   Connect to MCP server in stdio mode

Methods to be implemented by subclasses:
- register_server           Register MCP server
- get_available_tools       Get all available tools
- call_tool                 Call a tool

Implemented methods:
- _load_config              Load configuration
- process_llm_call          Call LLM (DeepSeek)
- process_tool_call         Tool call wrapper
- chat                      Main chat interaction entry point
"""

import json
import httpx
from typing import Dict, List, Optional
import yaml
from pathlib import Path

# Default config file path (project root)
DEFAULT_CONFIG_PATH = "config.yaml"

class MCPClient:
    """MCP Client class"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize MCP client
        
        Args:
            config_path: Path to config file, uses default if None
        """
        self.config_path = config_path or DEFAULT_CONFIG_PATH
        self.config = self._load_config()
        self.deepseek_api_key = self.config.get("deepseek_api_key")
        self.available_tools = []  # List of available tools

        if not self.deepseek_api_key:
            raise ValueError("DeepSeek API Key not configured, please set in config file")

    def register_server(self, server_url_or_path: str) -> bool:
        """
        Register MCP server

        Args:
            server_url_or_path: Server URL or path

        Returns:
            Whether registration succeeded
        """
        raise NotImplementedError

    async def get_available_tools(self) -> List[Dict]:
        """
        Get list of available tools from server
        
        Returns:
            List of tools
        """
        raise NotImplementedError

    async def call_tool(self, tool_name: str, arguments: Dict) -> Dict:
        """
        Call tool on MCP server

        Args:
            tool_name: Name of tool
            arguments: Tool arguments

        Returns:
            Tool call result
        """
        raise NotImplementedError

    def _load_config(self) -> Dict:
        """
        Load configuration file
        
        Returns:
            Configuration dictionary
        """
        config_path = Path(self.config_path)
        
        if not config_path.exists():
            # Create default config if file doesn't exist
            default_config = {
                "deepseek_api_key": "",
                "server_url": "http://localhost:8000"
            }
            
            with open(config_path, "w") as f:
                yaml.dump(default_config, f)
            
            print(f"Created default config file at {config_path}, please edit to add DeepSeek API Key")
            return default_config
        
        try:
            with open(config_path, "r") as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Failed to load config file: {e}")
            return {}

    async def process_llm_call(self, message: str, tools: List[Dict] = None) -> Dict:
        """
        Send request to DeepSeek API
        
        Args:
            message: User message
            tools: List of available tools
            
        Returns:
            DeepSeek response
        """
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.deepseek_api_key}",
            "Content-Type": "application/json"
        }
        
        # Build system prompt with tool information
        system_prompt = """You are an AI assistant that can use tools to help users:
{tools_info}

When you need to use a tool, respond in this format:
TOOL_CALL: {{"name": "tool_name", "arguments": {{"param_name": "param_value"}}}}

Important:
1. Tool calls must use the exact format above
2. Arguments must be valid JSON
3. Tool calls must be on a single line
4. Don't explain the tool call process, just return the tool call format
"""
        
        # Format tools information
        tools_info = "\n".join([
            f"- {tool['name']}: {tool['description']}\n  Parameters: {json.dumps(tool['parameters'], ensure_ascii=False)}"
            for tool in (tools or self.available_tools)
        ])
        
        system_prompt = system_prompt.format(tools_info=tools_info)
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            "stream": True
        }
        
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", url, headers=headers, json=data, timeout=60.0) as response:
                if response.status_code != 200:
                    error_text = await response.aread()
                    raise Exception(f"DeepSeek API error: {error_text}")
                
                full_response = ""
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        json_str = line[6:]
                        if json_str.strip() == "[DONE]":
                            break
                        
                        try:
                            chunk = json.loads(json_str)
                            delta = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            if delta:
                                full_response += delta
                                # Stream output
                                print(delta, end="", flush=True)
                        except json.JSONDecodeError:
                            pass
                
                print()  # New line
                return {"response": full_response}

    async def process_tool_call(self, response: str) -> Optional[str]:
        """
        Process tool call
        
        Args:
            response: DeepSeek response
            
        Returns:
            Tool call result or None
        """
        if "TOOL_CALL:" in response:
            try:
                # Extract tool call info
                tool_call_str = response.split("TOOL_CALL:")[1].strip()
                tool_call = json.loads(tool_call_str)
                
                tool_name = tool_call["name"]
                arguments = tool_call["arguments"]
                
                # Call the tool
                result = await self.call_tool(tool_name, arguments)
                
                # Return tool call result
                return json.dumps(result, ensure_ascii=False, indent=2)
            except Exception as e:
                return f"Failed to process tool call: {str(e)}"
        
        return None

    async def chat(self):
        """Interactive chat loop"""
        print("Welcome to HELLO-MCP client! Type 'exit' to quit.")

        # Get available tools list
        try:
            tools = await self.get_available_tools()
            self.available_tools = tools
            print("Available tools: ", self.available_tools)
        except Exception as e:
            print(f"Failed to get tools list: {str(e)}")
            return

        while True:
            user_input = input("\n> ")
            if user_input.lower() in ['exit', 'quit']:
                break

            try:
                # Send to DeepSeek to get response
                response_data = await self.process_llm_call(user_input, self.available_tools)
                response = response_data["response"]

                # Process tool call
                tool_result = await self.process_tool_call(response)
                if tool_result:
                    print("\nTool call result:")
                    print(tool_result)

                    # Send tool result back to DeepSeek for follow-up
                    follow_up = (
                        f"Tool call result:\n{tool_result}\n"
                        f"Please continue answering my question based on this result: {user_input}"
                    )

                    follow_response = await self.process_llm_call(follow_up, self.available_tools)

            except Exception as e:
                print(f"Error: {str(e)}")
            finally:
                # Ensure resources are released
                if hasattr(self, 'client') and hasattr(self.client, 'aclose'):
                    await self.client.aclose()  # Ensure client resources are released
