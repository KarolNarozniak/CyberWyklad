from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from app.app_agent.utils.tools.python_repl_tool import *
from app.app_agent.utils.prompts.prompts import *
from dotenv import load_dotenv
import os


load_dotenv()

# Pobierz klucz API z pliku .env
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY is not set in the .env file!")


llm = ChatAnthropic(model="claude-3-5-sonnet-latest", anthropic_api_key=ANTHROPIC_API_KEY)

translator_agent = create_react_agent(
    llm,
    [python_repl_tool],
    state_modifier=translator_prompt(
        "ile atomów ma wodór?"
    )
)

knowledge_agent = create_react_agent(
    llm,
    [python_repl_tool],
    state_modifier=knowledge_prompt(
        "How many atoms does hydrogen have?"
    )
)

planer_agent = create_react_agent(
    llm,
    [python_repl_tool],
    state_modifier=planer_prompt(
        "RAG DATA", "How many atoms does hydrogen have?"
    )
)

master_agent = create_react_agent(
    llm,
    [python_repl_tool],
    state_modifier=master_prompt(
        "planner's text"
    )
)

student_agent = create_react_agent(
    llm,
    [python_repl_tool],
    state_modifier=student_prompt(
        "master's text"
    )
)

equations_agent = create_react_agent(
    llm,
    [python_repl_tool],
    state_modifier=equations_prompt(
        "[CHEMISTRY, HYDROGEN, ATOMS]"
    )
)

slide_agent = create_react_agent(
    llm,
    [python_repl_tool],
    state_modifier=slide_prompt(
        r"{a^2 + b^2 = c^2, f(x) = \sum_{n=0}^\infty \frac{f^{(n)}(a)}{n!}(x-a)^n}", "master's text"
    )
)

translatorPolish_agent = create_react_agent(
    llm,
    [python_repl_tool],
    state_modifier=translatorPolish_prompt(
        "slide's content"
    )
)