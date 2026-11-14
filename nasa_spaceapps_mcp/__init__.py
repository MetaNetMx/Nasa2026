"""
NASA International Space Apps Challenge 2026 MCP Package.
Model Context Protocol server connecting to spaceappschallenge.org and NASA open data.
"""

from .server import mcp_server
from .client import SpaceAppsClient

__version__ = "2.0.0"
__all__ = ["mcp_server", "SpaceAppsClient"]
