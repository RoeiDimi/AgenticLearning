import asyncio
from fastmcp import FastMCP, Client

def test_tool_registration():
    mcp = FastMCP("TestMCP")

    @mcp.tool
    def add(a: int, b: int) -> int:
        return a + b

    async def run_client():
        async with Client(mcp) as client:
            result = await client.call_tool("add", {"a": 2, "b": 3})
            assert result.content[0].text == "5", f"Expected '5', got {result.content[0].text}"
            print("Tool dispatch test passed.")

    asyncio.run(run_client())

if __name__ == "__main__":
    test_tool_registration()
