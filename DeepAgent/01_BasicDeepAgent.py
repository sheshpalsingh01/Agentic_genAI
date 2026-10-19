"""
Deep Agents overview

Build agents that can plan, use subagents, and leverage file systems for complex tasks

deepagents is a standalone library for building agents that can tackle complex, multi-step tasks. Built on LangGraph and inspired by applications like Claude Code, Deep Research, and Manus, deep agents come with planning capabilities, file systems for context management, and the ability to spawn subagents.
When to use deep agents

Use deep agents when you need agents that can:

   -  Handle complex, multi-step tasks that require planning and decomposition
   -  Manage large amounts of context through file system tools
   - Delegate work to specialized subagents for context isolation
   - Persist memory across conversations and threads

"""

import os
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

from tavily import TavilyClient
from typing import Literal

tavily = TavilyClient(api_key=tavily_api_key)


def web_search(
    query: str,
    max_results: int = 5,
    topic: Literal["sport", "education", "newsfinance", "general"] = "general",
    include_raw_content: bool = False,
):
    """Run a websearch"""
    return tavily.search(
        query=query,
        max_results=max_results,
        topic=topic,
        include_raw_content=include_raw_content,
    )


# Create a Deep Agent
# Prompt
from deepagents import create_deep_agent
from langchain_groq import ChatGroq

llm = ChatGroq(model="qwen/qwen3.8-27b", api_key=groq_api_key)

deepAgent = create_deep_agent(
    model=llm,
    tools=[web_search],
    system_prompt="Act as a reseacher",
)

# agent
deepAgent


# basic agent
from langchain.agents import create_agent

agent = create_agent(
    model=llm, tools=[web_search], system_prompt="you are a researcher"
)
agent


# invoke the deepagent

response = deepAgent.invoke(
    {"messages": [{"role": "user", "content": "what is the langgraph"}]}
)
response['messages'][-1]

