#!/usr/bin/env python
"""
Top-level runner for NASA Space Apps Challenge 2026 MCP Server.
Usage:
  python run_mcp_server.py           # Runs in stdio mode (default for MCP clients)
  python run_mcp_server.py --test    # Runs diagnostic self-test
  python run_mcp_server.py --sse     # Runs SSE web server on port 8000
"""

import sys
import argparse
import asyncio
from nasa_spaceapps_mcp.server import mcp_server

def run_diagnostics():
    print("=" * 60)
    print("NASA Space Apps Challenge 2026 MCP Server - Diagnostics")
    print("=" * 60)
    
    async def _test():
        tools = await mcp_server.list_tools()
        resources = await mcp_server.list_resources()
        prompts = await mcp_server.list_prompts()
        
        print(f"Server Name: {mcp_server.name}")
        print(f"Registered Tools ({len(tools)}):")
        for t in tools:
            print(f"  - {t.name}: {t.description[:80]}...")
            
        print(f"\nRegistered Resources ({len(resources)}):")
        for r in resources:
            print(f"  - {r.uri}: {r.name}")
            
        print(f"\nRegistered Prompts ({len(prompts)}):")
        for p in prompts:
            print(f"  - {p.name}: {p.description}")
            
        print("\nTesting tool call 'list_challenges'...")
        from nasa_spaceapps_mcp.server import list_challenges
        res = list_challenges()
        print(f"  Found {len(res)} challenges in catalog!")
        for c in res[:3]:
            print(f"    * {c['title']} ({c['slug']})")
            
        print("\nTesting tool call 'solve_astronaut_health_problem'...")
        from nasa_spaceapps_mcp.server import solve_astronaut_health_problem
        res_med = solve_astronaut_health_problem()
        print(f"  Astronaut Mission Readiness Score: {res_med['mission_readiness_score']}% ({res_med['status']})")
        print(f"  Prescribed action: {res_med['priority_action_plan'][0]}")

        print("\nDiagnostics passed with 100% SUCCESS!")

    asyncio.run(_test())

def main():
    parser = argparse.ArgumentParser(description="NASA Space Apps 2026 MCP Server")
    parser.add_argument("--test", action="store_true", help="Run diagnostic test")
    parser.add_argument("--sse", action="store_true", help="Run SSE transport on port 8000")
    parser.add_argument("--port", type=int, default=8000, help="Port for SSE server")
    
    args = parser.parse_args()
    
    if args.test:
        run_diagnostics()
        return

    if args.sse:
        print(f"Starting NASA Space Apps 2026 MCP SSE Server on port {args.port}...")
        mcp_server.run(transport="sse")
    else:
        # Default: stdio transport for MCP clients
        mcp_server.run(transport="stdio")

if __name__ == "__main__":
    main()
