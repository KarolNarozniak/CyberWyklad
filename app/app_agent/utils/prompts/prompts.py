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
        "3. Finally, states \"do you have any questions?\""
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
