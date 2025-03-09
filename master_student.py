from typing_extensions import TypedDict
from typing import Literal
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END

llm = ChatOpenAI(model = "gpt-4o-mini")

class LecturePoint(TypedDict): #Lecture point w znaczeniu punkt wykladu - kolejne zagadnienie z tematu
	text: str
	topic: str
	question: str
	informative_or_not: str

class Feedback(BaseModel):
	grade: Literal["informative", "weak"] = Field(
		description = "Decide if the text is explained good enough"
	)
	question: str = Field(
		description = "If the text is not informative enough, ask a question about its contents"
	)
	
evaluator = llm.with_structured_output(Feedback)

def generate_text(state: LecturePoint):
	if state.get("question"):
		msg = llm.invoke(
			#f"Write a short text about the {state['topic']} as if you are a professor, but take into account the question: {state['question']}"
			f"""1. Begin the response by repeating \"{state['text']}\"
				2. anwser the question: {state['question']}"""
		)
	else:
		msg = llm.invoke(
			f"Write a 15 - word text about the {state['topic']} as if you are a professor" #10 wyrazow dla przykladu - aby evaluator mogl sie wykazac
		)
		print("master first text:" + msg.content + '\n')
	return {"text": msg.content}

def evaluate_text(state: LecturePoint):
	grade = evaluator.invoke(
		f"Grade the text {state['text']}"
	)
	print("student review/question:" + grade.grade + "/" + grade.question + "\n")
	return{"informative_or_not": grade.grade, "question": grade.question}

def route_text(state: LecturePoint):
    if state["informative_or_not"] == "informative":
        return "Accepted"
    elif state["informative_or_not"] == "weak":
        return "Rejected"
        
master_student = StateGraph(LecturePoint)
master_student.add_node("master", generate_text)
master_student.add_node("student", evaluate_text)

master_student.add_edge(START, "master")
master_student.add_edge("master", "student")
master_student.add_conditional_edges(
	"student",
	route_text,
	{
		"Accepted": END,
		"Rejected": "master"
	}
)

master_student_workflow = master_student.compile( )
#display(Image(master_student_workflow.get_graph().draw_mermaid_png( ))) #gdyby ktos chcial zobaczyc graf

wyklad = master_student_workflow.invoke({"topic": "what is a wave - particle duality?"})
print(wyklad["text"]) #finalny tekst