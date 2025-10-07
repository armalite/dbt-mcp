"""
Standalone FastMCP server with basic functionality
"""
try:
    from fastmcp import FastMCP
except ImportError:
    # Fallback to mcp.server.fastmcp if fastmcp not available
    from mcp.server.fastmcp import FastMCP

# Create a standalone FastMCP server
mcp = FastMCP("dbt-mcp-standalone")

@mcp.tool()
def test_connection() -> str:
    """Test that the server is running"""
    return "dbt-mcp server is running successfully"

@mcp.tool()
def server_status() -> dict:
    """Get server status and capabilities"""
    return {
        "server_type": "dbt-mcp-standalone",
        "status": "running",
        "capabilities": ["test_connection", "server_status", "placeholder_dbt_commands"],
        "message": "Server is running and ready for dbt operations"
    }

@mcp.tool()
def dbt_compile() -> dict:
    """Compile dbt models (placeholder)"""
    return {
        "status": "placeholder",
        "message": "dbt compile functionality will be added once base server is working",
        "command": "dbt compile"
    }

@mcp.tool()
def dbt_run() -> dict:
    """Run dbt models (placeholder)"""
    return {
        "status": "placeholder",
        "message": "dbt run functionality will be added once base server is working",
        "command": "dbt run"
    }

@mcp.tool()
def dbt_test() -> dict:
    """Run dbt tests (placeholder)"""
    return {
        "status": "placeholder",
        "message": "dbt test functionality will be added once base server is working",
        "command": "dbt test"
    }