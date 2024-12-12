import getpass
import os
from typing import Annotated, Literal
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langgraph.graph import MessagesState, END, StateGraph
from langgraph.types import Command
from IPython.display import Image, display

def _set_if_undefined(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"Please provide your {var}")

_set_if_undefined("ANTHROPIC_API_KEY")
_set_if_undefined("TAVILY_API_KEY")

tavily_tool = TavilySearchResults(max_results=5)
repl = PythonREPL()

@tool
def python_repl_tool(
    code: Annotated[str, "The python code to execute to generate your chart."],
):
    """Use this to execute python code. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user."""
    try:
        result = repl.run(code)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    result_str = f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"
    return (
        result_str + "\n\nIf you have completed all tasks, respond with FINAL ANSWER."
    )

def make_system_prompt(suffix: str) -> str:
    return (
        "You are a helpful AI assistant, collaborating with other assistants."
        " Use the provided tools to progress towards answering the question."
        " If you are unable to fully answer, that's OK, another assistant with different tools "
        " will help where you left off. Execute what you can to make progress."
        " If you or any of the other assistants have the final answer or deliverable,"
        " prefix your response with FINAL ANSWER so the team knows to stop."
        f"\n{suffix}"
    )

def translator_prompt(pytanie: str) -> str:
    return (
        "Q: Translate the sentence into English: czym jest kubit?"
        "A: What is a qubit?"
        "Q: Translate the sentence into English: na czym polega algorytm shora?"
        "A: What is Shor’s algorithm about?"
        f"Q: Translate the sentence into English: {pytanie}"
        "A: "
    )

def knowledge_prompt(question: str) -> str:
    return (
        "find the field and the most important elements of the text, write them in square brackets [ ]"
        "EXAMPLES:"
        "###"
        "Q: What is a qubit?"
        "A: [QUANTUM COMPUTING, QUBIT]"
        "Q: Which of the algorithms is better researched: Shor’s or Deutsch–Jozsa?"
        "A: [QUANTUM COMPUTING, SHOR'S ALGORITHM, DEUTSCH–JOZSA ALGORITHM]"
        "###"
        f"Q: {question}"
        "A: "
    )

def planer_prompt(data: str, question: str) -> str:
    return (
        "You are a professor. Your task is to create a plan for the lecture based on the question asked. To create the lecture, use only data delimited by ###. The plan is to be short and divided into numbered issues."
        "###"
        f"{data}"
        "###"
        f"Question: {question}"
    )

def master_prompt(problem: str) -> str:
    return (
        "Problem Statement:"
        f"1. {problem}"
        "If the problem is \"i don't have any questions\", skip solution and return \"OK\""
        "Solution Structure:"
        "1. Begin the response by repeating the problem enclosed in \" \""
        "2. Explain the problem, imagine yourself as a professor talking"
        "3. Finally, state \"do you have any questions?\""
    )

def student_prompt(text: str) -> str:
    return (
        "Read the text enclosed by ###,"
        "find a poorly explained topic in the text and ask them to re-write the prompt with a corrected topic"
        "If you have found no poorly explained topic, return \"I don’t have any questions\""
        "###"
        f"{text}"
        "###"
    )

def equations_prompt(knowledgeList: str) -> str:
    return (
        "write in LaTeX all the unique equations that you find in square brackets [ ]."
        "If there are no equations, leave the { } brackets empty."
        "EXAMPLES:"
        "###"
        "[NUMBER THEORY, EULER’S TOTIENT FUNCTION, EULER’S FORMULA, RIEMANN ZETA FUNCTION]"
        "{\\phi(n) = n \\prod_{p \\mid n} \\left(1 - \\frac{1}{p}\\right), e^{i\\theta} = \\cos\\theta + i\\sin\\theta,  \\zeta(s) = \\sum_{n=1}^\\infty \\frac{1}{n^s}, \\quad \\text{for } \\text{Re}(s) > 1}"
        "[QUANTUM MECHANICS, SCHRÖDINGER EQUATION, WAVE FUNCTION, ERWIN SCHRÖDINGER, NOBEL PRIZE]"
        "{I\\hbar \\frac{\\partial \\psi(\\mathbf{r}, t)}{\\partial t} = \\hat{H} \\psi(\\mathbf{r}, t)}"
        "[QUANTUM COMPUTING, NOISE]"
        "{ }"
        "###"
        f"{knowledgeList}"
    )

def slide_prompt(equations: str, text: str) -> str:
    return (
        "Your task is to format the text according to the instructions:"
        "1. Return the text enclosed by ### unmodified"
        "2. If any of the equations found in { } correspond to text found in ###, output them below the text"
        "###"
        f"{text}"
        "###"
        f"{equations}"
    )

def translatorPolish_prompt(slide: str) -> str:
    return (
        "Q: Translate the text into Polish: What is a qubit?"
        "A: czym jest kubit?"
        "Q: Translate the text into Polish: What is Shor’s algorithm about?"
        "A: na czym polega algorytm Shora?"
        f"Q: Translate the sentence into Polish: {slide}"
        "A: "
    )

llm = ChatAnthropic(model="claude-3-5-sonnet-latest")

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

def get_next_node(last_message: BaseMessage, goto: str):
    if "FINAL ANSWER" in last_message.content:
        return END
    return goto

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

def master_node(state: MessagesState) -> Command[Literal["student", END]]:
    result = master_agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "student")
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content, name="master"
    )
    return Command(
        update={"messages": result["messages"]},
        goto=goto,
    )

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

def slide_node(state: MessagesState) -> Command[Literal["translatorPolish", END]]:
    result = slide_agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "translatorPolish")
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content, name="slide"
    )
    return Command(
        update={"messages": result["messages"]},
        goto=goto,
    )

def translatorPolish_node(state: MessagesState) -> Command[Literal[END]]:
    result = translatorPolish_agent.invoke(state)
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content, name="translatorPolish"
    )
    return Command(
        update={"messages": result["messages"]},
        goto=END,
    )

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

graph = workflow.compile()

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
