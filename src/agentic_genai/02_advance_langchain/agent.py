import os
from typing import Annotated
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()


os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGSMITH_PROJECT"] = "debugginng"
os.environ["LANGSMITH_TRACING"] = "true"


# intialize llm
llm = init_chat_model("groq:qwen/qwen3.8-27b")


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


## Graph with tool call
def make_tool_graph():
    """Graph with tool call"""

    @tool
    def add(a: float, b: float) -> float:
        """Adding two number"""
        return a + b


    tool_node = ToolNode([add])

    llm_with_tool = llm.bind_tools([add])


    # tool dafination
    def tool_calling_llm(state: State):
        return {"messages": [llm_with_tool.invoke(state["messages"])]}


    # Graph
    builder = StateGraph(State)
    builder.add_node("tool_calling_llm", tool_calling_llm)
    builder.add_node("tools", ToolNode([add]))

    # Add edges
    builder.add_edge(START, "tool_calling_llm")
    builder.add_conditional_edges(
        "tool_calling_llm",
        tools_condition,
        {
            "tools": "tools",
            END: END,
        },
    )
    builder.add_edge("tools", "tool_calling_llm")

    # Compile graph
    graph = builder.compile()
    
    return graph

tool_agent =make_tool_graph()

