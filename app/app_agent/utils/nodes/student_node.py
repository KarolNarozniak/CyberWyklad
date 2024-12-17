from langgraph.graph import MessagesState, END, StateGraph
from langchain_core.messages import BaseMessage, HumanMessage
from typing import Literal
from langgraph.types import Command
from app.app_agent.utils.agents import *
from app.app_agent.utils.agents.agents import student_agent
from app.app_agent.utils.nodes.get_next_node import get_next_node


def student_node(state: MessagesState) -> Command[Literal["equations", END]]:
    result = student_agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "equations")
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content, name="student"
    )
    return Command(
        update={"messages": result["messages"]},
        goto=goto,
    )