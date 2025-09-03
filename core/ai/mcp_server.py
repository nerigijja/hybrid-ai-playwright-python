# mcp_server.py
import asyncio
from mcp.server.fastmcp import FastMCP
import mcp.types as types

mcp = FastMCP("Test Automation MCP")

@mcp.tool()
def run_test(test_id: str) -> str:
    # Hook into your pytest runner
    import subprocess
    result = subprocess.run(
        ["pytest", f"--maxfail=1", "-q", f"tests/{test_id}.py"],
        capture_output=True, text=True
    )
    return result.stdout or result.stderr

@mcp.tool()
def get_logs(service: str) -> str:
    # e.g., collect logs or report
    with open("artifacts/test-report.html") as f:
        return f.read()

if __name__ == "__main__":
    asyncio.run(mcp.run(transport="stdio"))
