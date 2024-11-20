import os
from typing import List
from openai import OpenAI
import re

'''
Dane są dzielone na podstawie znacznika, obecny znacznik to "------>[cos]<------"
cos - to domyślnie bedzie temat prezentacji
'''

class Filter:
    def __init__(self, profesor_input: str, model_name: str, **openai_client_args) -> None:
        self.profesor_input = profesor_input
        # znacznik: # ------>[tytuł slajdu]<------
        self.split_mark = r"------>\[.*?\]<------"
        self.text_chunks = []
        self.presentation_chunks = []
        self.txt_for_LaTeX = ""
        self.openai_client_args = openai_client_args
        self.model_name = model_name

    def run(self):
        self.split_presentations()
        self.extract_chunks_topics()
        self.write_in_points_text_chunk()
        return self.get_output()

    def split_presentations(self):
        chunks = re.split(self.split_mark, self.profesor_input)
        self.text_chunks = [chunk.strip() for chunk in chunks if chunk.strip()]


    def extract_chunks_topics(self):
        self.presentation_chunks = re.findall(self.split_mark, self.profesor_input)

    '''
     udało się niestety usunąć każdorazowego wprowadzenia do tematu przez AI np.:
    * Splątanie is a quantum phenomenon where two objects become connected in such a way that their state depends 
    on each other's state, regardless of distance.
    * Einstein first described it as "an extraordinary happening at a distance".
    * In practice, splątanie can be used for rapid data transfer - but this is often misunderstood and misinterpreted 
    in popular culture.
    * Splątanie has immense potential in cryptography, allowing for theoretically unbreakable encryption systems
    Dlatego za każdym razem pomijana jest pierwsza linia
    ToDo: Napisać tak aby sam llm pisał bez pierwszej linię
    '''

    def write_in_points_text_chunk(self):
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'), **self.openai_client_args)
        i = 0
        for txt in self.text_chunks:
            completion = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": f"List me the key points from this text: {txt}"}
                ],
            )
            self.txt_for_LaTeX += "\n\n"
            self.txt_for_LaTeX += self.presentation_chunks[i]
            self.txt_for_LaTeX += "\n"
            response_in_lines = completion.choices[0].message.content.splitlines()
            filtered_response = "\n".join(response_in_lines[1:])
            self.txt_for_LaTeX += filtered_response
            i += 1

            # print(completion.choices[0].message.content)

    def get_output(self):
        return self.txt_for_LaTeX

    # Komenda dla modułu TTS
    def get_presentations_splited(self):
        self.split_presentations()
        return self.text_chunks


if __name__ == "__main__":
    ###################
    # Przykład użycia #
    ###################
    example_file_path = os.path.join("input_data", "text_example")
    with open(example_file_path, 'r', encoding='utf-8') as file:
        text_example = file.read()

    filter_agent = Filter(text_example)


    filter_output = filter_agent.run()
    print(filter_output)
