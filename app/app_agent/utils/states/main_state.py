from langgraph.graph import StateGraph, MessagesState

from app.app_agent.utils.nodes.equations_node import equations_node
from app.app_agent.utils.nodes.knowledge_node import knowledge_node
from app.app_agent.utils.nodes.master_node import master_node
from app.app_agent.utils.nodes.planner_node import planner_node
from app.app_agent.utils.nodes.slide_node import slide_node
from app.app_agent.utils.nodes.student_node import student_node
from app.app_agent.utils.nodes.translatorPolish_node import translatorPolish_node
from app.app_agent.utils.nodes.translator_node import translator_node


def create_workflow():
    workflow = StateGraph(MessagesState)

    workflow.add_node("translator", translator_node)
    workflow.add_node("knowledge", knowledge_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("master", master_node)
    workflow.add_node("student", student_node)
    workflow.add_node("equations", equations_node)
    workflow.add_node("slide", slide_node)
    workflow.add_node("translatorPolish", translatorPolish_node)

    workflow.set_entry_point("translator")

    workflow.add_edge("translator", "knowledge")
    workflow.add_edge("knowledge", "planner")
    workflow.add_edge("planner", "master")

    N = 3
    for _ in range(N):
        workflow.add_edge("master", "student")
        workflow.add_edge("student", "master")

    workflow.add_edge("master", "slide")
    workflow.add_edge("equations", "slide")
    workflow.add_edge("slide", "translatorPolish")

    return workflow.compile()
