"""
Pure FastMCP server to avoid asyncio conflicts with dbt-mcp
"""
from mcp.server.fastmcp import FastMCP

# Create a pure FastMCP server without any dbt-mcp imports
mcp = FastMCP("dbt-mcp-pure")

@mcp.tool()
def test_connection() -> str:
    """Test that the server is running"""
    return "dbt-mcp server is running in pure FastMCP mode"

@mcp.tool()
def server_info() -> dict:
    """Get server information"""
    return {
        "server_type": "pure-fastmcp",
        "status": "running",
        "message": "This is a minimal FastMCP server without dbt-mcp imports to avoid asyncio conflicts"
    }