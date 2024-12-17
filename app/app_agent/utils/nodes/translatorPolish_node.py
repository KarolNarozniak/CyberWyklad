from langgraph.graph import MessagesState, END, StateGraph
from langchain_core.messages import BaseMessage, HumanMessage
from typing import Literal
from langgraph.types import Command
from app.app_agent.utils.agents import *
from app.app_agent.utils.agents.agents import translatorPolish_agent


def translatorPolish_node(state: MessagesState) -> Command[Literal[END]]:
    result = translatorPolish_agent.invoke(state)
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content, name="translatorPolish"
    )
    return Command(
        update={"messages": result["messages"]},
        goto=END,
    )