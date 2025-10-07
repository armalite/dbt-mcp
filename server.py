"""
FastMCP-compatible entry point for dbt-mcp
"""
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

from mcp.server.lowlevel.server import LifespanResultT
from dbt_mcp.config.config import load_config
from dbt_mcp.mcp.server import DbtMCP
from dbt_mcp.tracking.tracking import UsageTracker
from dbt_mcp.dbt_admin.tools import register_admin_api_tools
from dbt_mcp.dbt_cli.tools import register_dbt_cli_tools
from dbt_mcp.dbt_codegen.tools import register_dbt_codegen_tools
from dbt_mcp.discovery.tools import register_discovery_tools
from dbt_mcp.semantic_layer.client import DefaultSemanticLayerClientProvider
from dbt_mcp.semantic_layer.tools import register_sl_tools
from dbt_mcp.sql.tools import register_sql_tools, SqlToolsManager

# Load config
config = load_config()

@asynccontextmanager
async def fastmcp_lifespan(server: DbtMCP) -> AsyncIterator[None]:
    """FastMCP-compatible lifespan that includes tool registration"""
    # Register all tools during startup
    if config.semantic_layer_config_provider:
        register_sl_tools(
            server,
            config_provider=config.semantic_layer_config_provider,
            client_provider=DefaultSemanticLayerClientProvider(
                config_provider=config.semantic_layer_config_provider,
            ),
            exclude_tools=config.disable_tools,
        )

    if config.discovery_config_provider:
        register_discovery_tools(
            server, config.discovery_config_provider, config.disable_tools
        )

    if config.dbt_cli_config:
        register_dbt_cli_tools(server, config.dbt_cli_config, config.disable_tools)

    if config.dbt_codegen_config:
        register_dbt_codegen_tools(
            server, config.dbt_codegen_config, config.disable_tools
        )

    if config.admin_api_config_provider:
        register_admin_api_tools(
            server, config.admin_api_config_provider, config.disable_tools
        )

    if config.sql_config_provider:
        await register_sql_tools(
            server, config.sql_config_provider, config.disable_tools
        )

    try:
        yield
    finally:
        # Cleanup
        try:
            await SqlToolsManager.close()
        except Exception:
            pass

# Create DbtMCP instance with tool registration lifespan
mcp = DbtMCP(
    config=config,
    usage_tracker=UsageTracker(),
    name="dbt",
    lifespan=fastmcp_lifespan,
)