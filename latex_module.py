import tempfile
from pdf2image import convert_from_bytes
from openai import OpenAI
import subprocess
import os

class Latex_module:
    def __init__(self, presentation_text: str, model: str, 
                 output_prefix: str = "slide", **openai_args) -> None:
        self.output_prefix: str = output_prefix
        self.presentation_text: str = presentation_text
        self.model_name: str = model
        self.openai_args: dict[str, str] = openai_args
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'), **openai_args)
        self.prompt = (f"Create a LaTeX presentation using beamer library from the following text:\n\n{self.presentation_text}\n\n"
                       "Make sure to use \\usepackage[T1]{fontenc}, and for the actual content to be in polish language.\n")

    def get_latex(self) -> str:
        """
        This function gets the LaTeX code for the presentation.
        """
        response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": self.prompt},
                ],
                temperature=0.7,
            max_tokens=1000
            )
        return response.choices[0].message.content

    
    def generate_pngs(self, response: str) -> None:
        """
        This function generates PNG images for each slide of the presentation.
        First it generates the PDF file then converts it to PNG images.
        """

        print(response)


        with tempfile.TemporaryDirectory() as tempdir:
            tex_file_path = os.path.join(tempdir, "presentation.tex")
            pdf_file_path = os.path.join(tempdir, "presentation.pdf")

            # Write LaTeX code to a .tex file
            with open(tex_file_path, 'w') as tex_file:
                tex_file.write(response.split("```")[1][5:-1])

            # Use subprocess to call pdflatex and generate the PDF
            subprocess.run(['latexmk', '-pdf', '-output-directory=' + tempdir, tex_file_path], check=True)

            # Read the generated PDF file
            with open(pdf_file_path, 'rb') as pdf_file:
                pdf_bytes = pdf_file.read()

            # Convert PDF bytes to PNG
            images = convert_from_bytes(pdf_bytes)
            for i, image in enumerate(images):
                image.save(f"{self.output_prefix}_{i+1}.png", 'PNG')

    def run(self) -> None:
        """
        This function runs the module.
        """
        while True: # TODO do not leave this in
            try:
                response = self.get_latex()
                self.generate_pngs(response)
                print("Done!")
                break
            except Exception as e:
                print(f"Error: {e}")
                continue