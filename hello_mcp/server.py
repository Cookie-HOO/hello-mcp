"""
MCP Server Module
Simple MCP server built with FastMCP, provides file listing tool

Method 1: Start in SSE mode (default listens on 127.0.0.1:8000)
    python -m hello_mcp.server --transport sse

Method 2: Start in stdio mode
    python -m hello_mcp.server
"""
import argparse
import logging
import os
from typing import Dict
import uvicorn
from mcp.server.fastmcp import FastMCP
from fastapi import HTTPException
from fastapi import FastAPI
from pydantic import Field


# Initialize global variables
app = FastAPI()  # for sse
logger = logging.getLogger("mcp")
mcp = FastMCP("hello-mcp")
tool_manager = mcp._tool_manager


@mcp.tool(name="list_dir", description="List all files in specified directory")
async def list_dir(
        dir_path: str = Field(description="Directory path"),
):
    try:
        dir_path = os.path.expanduser(dir_path)  # Expand ~ to full path
        if not os.path.exists(dir_path):
            return {"error": f"Path does not exist: {dir_path}"}
        if not os.path.isdir(dir_path):
            return {"error": f"Not a directory, path required: {dir_path}"}

        # If directory, return its contents
        files = []
        for item in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item)
            item_type = "directory" if os.path.isdir(item_path) else "file"
            files.append({"name": item, "type": item_type})
        return {"type": "directory", "path": dir_path, "contents": files}
    except Exception as e:
        return {"error": f"Failed to read path: {str(e)}"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.get("/tools")
async def get_tools():
    """Get all available tools"""
    tools = []
    for tool in tool_manager.list_tools():
        tools.append({
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.parameters
        })
    return tools

@app.post("/tools/{tool_name}")
async def call_tool(tool_name: str, arguments: Dict):
    """Call specified tool"""
    tool = tool_manager.get_tool(tool_name)
    if tool is None:
        raise HTTPException(status_code=404, detail=f"Tool {tool_name} not found")
    
    try:
        result = await tool_manager.call_tool(tool_name, arguments)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def main():
    """Command line entry point"""
    parser = argparse.ArgumentParser(description="MCP Server")
    parser.add_argument("--transport", "-t", help="Transport protocol: stdio|sse", default="stdio")
    parser.add_argument("--listen", "-l", help="Listen address (SSE mode only), default: 127.0.0.1:8000", default="127.0.0.1:8000")

    args = parser.parse_args()

    if args.transport == "stdio":
        logger.info("Starting MCP service in stdio mode")
        mcp.run(transport="stdio")

    elif args.transport == "sse":
        host, port = args.listen.split(":")
        # Using uvicorn instead of native mcp to extend functionality
        # GET /health
        # GET /tools
        # POST /tools/{tool_name}
        logger.info(f"Starting MCP service in SSE mode, listening on {host}:{port}")
        uvicorn.run(app, host=host, port=int(port))
    else:
        raise ValueError("Invalid transport, only supports: stdio, sse")


if __name__ == "__main__":
    main()
