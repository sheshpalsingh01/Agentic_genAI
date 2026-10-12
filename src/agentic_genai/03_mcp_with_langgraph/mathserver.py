from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a:int,b:int)->int:
    """_Summary_
    add to number"""
    return a+b

@mcp.tool()
def multiple(a:int,b:int)->int:
    """Multiple two number"""
    return a*b

if __name__=="__main__":
    mcp.run(transport="stdio") 
    
# transport="stdio" argument tells the server to
# Use standrad input/output (stdin and stdout) to recieve and respond to tool function callls