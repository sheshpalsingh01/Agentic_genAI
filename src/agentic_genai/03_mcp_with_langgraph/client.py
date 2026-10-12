from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
import os
import asyncio

async def main():
    client = MultiServerMCPClient(
        {
            "math":{
                "command":"python",
                "args":["mathserver.py"], # absulute file path
                "transport":"stdio"
            },
            "weather":{
                "url":"http://127.0.0.1:8000/mcp",
                'transport':'streamable_http'
            }
        }
    )
    
    os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
    
    tool =  await client.get_tools()
    model = ChatGroq(model ="qwen/qwen3.8-27b")
    agent = create_react_agent(
        model=model,
        tools= tool
    )
    
    math_response = await agent.ainvoke(
        {"messages":[{'role':'user',"content":"what is the(3+4)*3"}]}
    )
    
    weather_response = await agent.ainvoke(
        {"messages":[{'role':'user',"content":"what is weather in california"}]}
    )
    print("wather response",weather_response['messages'][-1].content)
    print("math response :", math_response['messages'][-1].content)

asyncio.run(main=main())