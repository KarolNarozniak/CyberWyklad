from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from app.app_agent.utils.agents.agents import *
from app.app_agent.utils.nodes.get_next_node import *


def knowledge_node(state: MessagesState) -> Command[Literal["planner", END]]:
    result = knowledge_agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "planner")
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content, name="knowledge"
    )
    return Command(
        update={"messages": result["messages"]},
        goto=goto,
    )