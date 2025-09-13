
import json
from fastmcp import FastMCP

mcp = FastMCP("LambdaMCP")

# Register a sample add tool
@mcp.tool
def add(a: float, b: float) -> float:
    """Returns the sum of a and b."""
    return a + b

# Example resource
@mcp.resource("config://version")
def get_version():
    return "2.0.1"

# Example prompt
@mcp.prompt
def greet(name: str) -> str:
    return f"Hello, {name}!"

import asyncio
from fastmcp import Client

def dispatch_mcp_request(mcp, request: dict):
    method = request.get("method")
    params = request.get("params", {})

    async def run_client():
        async with Client(mcp) as client:
            # Try tool
            try:
                result = await client.call_tool(method, params)
                # For tools, result.content[0].text is the string output
                return {"type": "tool", "result": result.content[0].text}
            except Exception:
                pass
            # Try resource
            try:
                result = await client.call_resource(method, params)
                return {"type": "resource", "result": result.content[0].text}
            except Exception:
                pass
            # Try prompt
            try:
                result = await client.call_prompt(method, params)
                return {"type": "prompt", "result": result.content[0].text}
            except Exception:
                pass
            return {"error": f"Unknown method: {method}"}

    return asyncio.run(run_client())

def handler(event, context):
    try:
        # Log available tool names for debugging
        print("Registered tools:", list(getattr(mcp, "tools", {}).keys()))
        body = event.get("body")
        if body is None:
            return {"statusCode": 400, "body": json.dumps({"error": "Missing request body"})}
        request = json.loads(body)
        response = dispatch_mcp_request(mcp, request)
        return {"statusCode": 200, "body": json.dumps(response), "headers": {"Content-Type": "application/json"}}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
