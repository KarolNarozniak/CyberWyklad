import os
os.environ["OPENAI_API_KEY"] = " "

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model = "gpt-4o-mini")

from langchain_core.prompts import ChatPromptTemplate
class Translator:
	fewshotknow = [
		{
			"question": "czym jest kubit?",
			"answer": "What is a qubit?"
		},
		{
			"question": "na czym polega algorytm shora?",
			"answer": "What is Shor’s algorithm about?"
		}
	]
	def __init__(self):
		self.prompt = PromptTemplate.from_template(
			"Translate the following into English\n{question}\n{answer}"
		)
		self.translator_template = FewShotPromptTemplate(
    		examples = self.fewshotknow,
    		example_prompt = self.prompt,
    		suffix = "{text}",
    		input_variables = ["text"]
		)

	def invoke(self, question):
		prompt = self.translator_template.invoke({"text": question})
		print("tlumacz: co przetwarzam\n", prompt.to_string( ), "\n")
		return llm.invoke(prompt).content

from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
class Knowledge:
	fewshotknow = [
		{
			"question": "What is a qubit?",
			"answer": "[QUANTUM COMPUTING, QUBIT]"
		},
		{
			"question": "Which of the algorithms is better researched: Shor’s or Deutsch–Jozsa?",
			"answer": "[QUANTUM COMPUTING, SHOR'S ALGORITHM, DEUTSCH–JOZSA ALGORITHM]"
		},
		{
			"question": "Can the Pythagorean theorem be proven using sine and cosine?",
			"answer": "[MATHEMATICS, TRIGONOMETRY, PYTHAGOREAN THEOREM, SINE, COSINE]"
		}
	]
	def __init__(self):
		self.prompt = PromptTemplate.from_template(
			"find the field and the most important elements of the text, write them in square brackets [ ]\n{question}\n{answer}"
		)
		self.knowledge_template = FewShotPromptTemplate(
    		examples = self.fewshotknow,
    		example_prompt = self.prompt,
    		suffix = "find the field and the most important elements of the text, write them in square brackets[ ]\n{text}",
    		input_variables = ["text"]
		)
	def invoke(self, question):
		prompt = self.knowledge_template.invoke({"text": question})
		print("wiedza: oto co przetwarzam\n", prompt.to_string( ))
		return llm.invoke(prompt).content