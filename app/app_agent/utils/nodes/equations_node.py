from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from app.app_agent.utils.agents.agents import *
from app.app_agent.utils.nodes.get_next_node import *


def equations_node(state: MessagesState) -> Command[Literal["slide", END]]:
    result = equations_agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "slide")
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content, name="equations"
    )
    return Command(
        update={"messages": result["messages"]},
        goto=goto,
    )