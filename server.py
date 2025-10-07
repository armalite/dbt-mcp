"""
FastMCP-compatible entry point for dbt-mcp
"""
from contextlib import asynccontextmanager
from typing import AsyncIterator

@asynccontextmanager
async def simple_lifespan(server) -> AsyncIterator[None]:
    """Simple lifespan without complex tool registration"""
    try:
        yield
    finally:
        pass

# Import only at the very end to minimize asyncio conflicts
try:
    from dbt_mcp.mcp.server import DbtMCP
    from dbt_mcp.tracking.tracking import UsageTracker

    class MinimalConfig:
        """Minimal config for initialization"""
        def __init__(self):
            self.semantic_layer_config_provider = None
            self.discovery_config_provider = None
            self.dbt_cli_config = None
            self.dbt_codegen_config = None
            self.admin_api_config_provider = None
            self.sql_config_provider = None
            self.disable_tools = []
            self.tracking_config = None

    # Create DbtMCP instance with minimal setup
    mcp = DbtMCP(
        config=MinimalConfig(),
        usage_tracker=UsageTracker(),
        name="dbt",
        lifespan=simple_lifespan,
    )
except Exception as e:
    print(f"Error creating dbt-mcp server: {e}")
    # Create a minimal FastMCP server as fallback
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("dbt-fallback")

    @mcp.tool()
    def test_tool() -> str:
        """Test tool to verify server is working"""
        return "dbt-mcp server is running in fallback mode"