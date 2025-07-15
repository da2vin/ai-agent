#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


if __name__ == "__main__":
    # mcp.settings.host = "0.0.0.0"
    mcp.settings.port = 8111
    mcp.run(transport="sse")

    # https://github.com/modelcontextprotocol/python-sdk
    # https://modelcontextprotocol.io/introduction
    # uv run mcp dev .\mcps\demo_server.py
