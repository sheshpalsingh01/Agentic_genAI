import os
from dotenv import load_dotenv

load_dotenv()

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq


class State(TypedDict):
    """Messgas have the 'list[dict[str,str]]. that add_messages function
    in the annotated defines how this state key should be update.
    in this case it appends the new  messages to the existing list of messages
    """

    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# =======================================
# LLM
# =======================================

llm = ChatGroq(model="qwen/qwen3.8-27b", temperature=0.7)

# ========================================
# Node functionality
# ========================================


def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


# Adding Node to the graph
graph_builder.add_node('llmchatbot',chatbot)

# Adding edge to the graph
graph_builder.add_edge(START,'llmchatbot')
graph_builder.add_edge('llmchatbot',END)

graph = graph_builder.compile()



user_inoput=input("Enter the messges : ")

for event in graph.stream({'messages':user_inoput}):
    for message in event.values():
        print(message['messages'][-1].content)