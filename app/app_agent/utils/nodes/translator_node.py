from langgraph.graph import MessagesState, END, StateGraph
from langchain_core.messages import BaseMessage, HumanMessage
from typing import Literal
from langgraph.types import Command
from app.app_agent.utils.agents import *
from app.app_agent.utils.agents.agents import translator_agent
from app.app_agent.utils.nodes.get_next_node import get_next_node


def translator_node(state: MessagesState) -> Command[Literal["knowledge", END]]:
    result = translator_agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "knowledge")
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content, name="translator"
    )
    return Command(
        update={"messages": result["messages"]},
        goto=goto,
    )