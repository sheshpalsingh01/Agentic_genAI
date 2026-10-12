from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")

@mcp.tool()
async def get_weather(location:str) -> str:
    """ Get the weather location.
    """
    return "it's always raining in california"

if __name__=="__main__":
    mcp.run(transport="streamable-http")
    
# Using transport="streamable-http" (or simply transport="http" in newer versions)
# transitions your Model Context Protocol (MCP) server from a local desktop script 
# into a live web API service.