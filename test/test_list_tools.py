import asyncio
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

async def main():
    try:
        async with sse_client("https://binance.armaddia.lat/sse") as streams:
            async with ClientSession(streams[0], streams[1]) as session:
                await session.initialize()
                
                print("--- Available MCP Tools ---")
                tools_response = await session.list_tools()
                for tool in tools_response.tools:
                    print(f"Tool Name: {tool.name}")
                    print(f"Description: {tool.description}")
                    print("-" * 40)
                    
    except Exception as e:
        print(f"Error connecting to server: {e}")

if __name__ == "__main__":
    asyncio.run(main())