from langgraph.graph import MessagesState, END, StateGraph
from langchain_core.messages import BaseMessage, HumanMessage
from typing import Literal
from langgraph.types import Command
from app.app_agent.utils.agents import *
from app.app_agent.utils.agents.agents import planer_agent
from app.app_agent.utils.nodes.get_next_node import *


def planner_node(state: MessagesState) -> Command[Literal["master", END]]:
    result = planer_agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "master")
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content, name="planner"
    )
    return Command(
        update={"messages": result["messages"]},
        goto=goto,
    )