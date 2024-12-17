import os
import getpass

from dotenv import load_dotenv

from app.app_agent.utils.states.main_state import create_workflow
from IPython.display import Image, display


def _set_if_undefined(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"Please provide your {var}")


# if __name__=="__main__":
def run_cyber_wyklad():
    print("Start")
    load_dotenv()

    _set_if_undefined("ANTHROPIC_API_KEY")
    _set_if_undefined("TAVILY_API_KEY")


    graph = create_workflow()

    try:
        img_data = graph.get_graph().draw_mermaid_png()
        display(Image(img_data))
    except Exception as e:
        print(f"An error occurred: {e}")

    events = graph.stream(
        {
            "messages": [
                (
                    "user",
                    "Daj mi 1000 slow prezentacje na poziomie wprowadzajacym pod tytulem: Czym jest kubit i jakie ma zastosowanie w kryptologii kwantowej? Nie pytaj mnie o nic, sam podjemij decyzje jak to powinno wygladac, zrob tak zeby bylo dobrze",
                )
            ],
        },
        {"recursion_limit": 150},
    )
    for s in events:
        print(s)
        print("----")
