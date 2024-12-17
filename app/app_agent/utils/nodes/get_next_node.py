from langgraph.graph import END
from langchain_core.messages import BaseMessage


def get_next_node(last_message: BaseMessage, goto: str):
    if "FINAL ANSWER" in last_message.content:
        return END
    return goto