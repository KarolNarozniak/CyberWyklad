from langgraph.graph import MessagesState, END, StateGraph
from langchain_core.messages import BaseMessage, HumanMessage
from typing import Literal
from langgraph.types import Command
from app.app_agent.utils.agents.agents import *
from app.app_agent.utils.nodes.get_next_node import *


def master_node(state: MessagesState) -> Command[Literal["student", END]]:
    result = master_agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "student")
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content, name="master"
    )
    return Command(
        update={"messages": result["messages"]},
        goto=goto,
    )