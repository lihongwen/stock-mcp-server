"""MCP server entry point for Stock MCP Server."""

import asyncio
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, Resource
from loguru import logger

from stock_mcp_server.config import get_config
from stock_mcp_server.resources import list_resources, read_resource
from stock_mcp_server.tools.market_data import get_market_data
from stock_mcp_server.utils.logger import setup_logging


def create_server() -> Server:
    """Create and configure the MCP server."""
    config = get_config()
    server = Server(config.server_name)

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available MCP tools."""
        return [
            Tool(
                name="get_market_data",
                description="获取市场数据（实时行情/市场宽度/资金流向）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "data_type": {
                            "type": "string",
                            "enum": ["realtime", "breadth", "capital_flow", "all"],
                            "description": "数据类型：realtime(实时行情), breadth(市场宽度), capital_flow(资金流向), all(全部)",
                            "default": "realtime",
                        },
                        "index_code": {
                            "type": "string",
                            "description": "指数代码，默认 000001（上证指数）",
                            "default": "000001",
                        },
                        "date": {
                            "type": "string",
                            "description": "交易日期（YYYY-MM-DD格式），可选，默认最新交易日",
                        },
                    },
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: Any) -> list[TextContent]:
        """Handle tool calls."""
        try:
            logger.info(f"Tool called: {name} with arguments: {arguments}")

            if name == "get_market_data":
                result = await get_market_data(arguments)
                return [TextContent(type="text", text=str(result))]

            return [
                TextContent(
                    type="text",
                    text=f"Unknown tool: {name}",
                )
            ]

        except Exception as e:
            logger.error(f"Error executing tool {name}: {e}")
            return [
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}",
                )
            ]

    @server.list_resources()
    async def handle_list_resources() -> list[Resource]:
        """List available MCP resources."""
        resources_list = list_resources()
        return [
            Resource(
                uri=res["uri"],
                name=res["name"],
                description=res["description"],
                mimeType=res["mimeType"],
            )
            for res in resources_list
        ]

    @server.read_resource()
    async def handle_read_resource(uri: str) -> str:
        """Read a resource by URI."""
        try:
            logger.info(f"Reading resource: {uri}")
            result = read_resource(uri)
            
            # Return JSON string representation
            import json
            return json.dumps(result, ensure_ascii=False, indent=2)
            
        except Exception as e:
            logger.error(f"Error reading resource {uri}: {e}")
            import json
            return json.dumps({
                "error": {
                    "code": "RESOURCE_ERROR",
                    "message": str(e),
                }
            }, ensure_ascii=False)

    logger.info(f"MCP server '{config.server_name}' created with 10 tools and 10 resources")
    return server


async def run_server() -> None:
    """Run the MCP server with stdio transport."""
    setup_logging()
    logger.info("Starting Stock MCP Server...")

    server = create_server()

    async with stdio_server() as (read_stream, write_stream):
        logger.info("Server running on stdio transport")
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main() -> None:
    """Main entry point."""
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise


if __name__ == "__main__":
    main()
