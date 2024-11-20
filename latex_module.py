import tempfile
from pdf2image import convert_from_bytes
from openai import OpenAI
import subprocess
import os

class LatexModule:
    def __init__(self, presentation_text: str, model: str,
                 output_filename_prefix: str = "slide", output_dir: str = "output" , **openai_client_args) -> None:
        self.output_filename_prefix: str = output_filename_prefix
        self.presentation_text: str = presentation_text
        self.model_name: str = model
        self.output_dir: str = output_dir
        self.openai_client_args: dict[str, str] = openai_client_args
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'), **openai_client_args)
        self.prompt = ("Create a LaTeX presentation using beamer library. Make sure to use \\usepackage[T1]{fontenc}, "
                       "and for the actual content to be in polish language. "
                       "Do not include ANY output other than latex code or kittens will die.\n"
                       f"Use the following text:\n\n{self.presentation_text}\n\n")

    def get_latex(self) -> str:
        """
        This function gets the LaTeX code for the presentation.
        """
        response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": self.prompt},
                ],
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

            #step 1: usuniecie wszystkiego do pierwszego \
            response: str = '\\' + "\\".join(response.split("\\")[1:])
            print("Modified response:")
            print(response)

            # Write LaTeX code to a .tex file
            with open(tex_file_path, 'w') as tex_file:
                tex_file.write(response)
                # tex_file.write(response.split("```")[1][5:-1])

            subprocess.run(['latexmk', '-pdf', "-interaction=nonstopmode", '-output-directory=' + tempdir, tex_file_path], check=True)

            # Read the generated PDF file
            with open(pdf_file_path, 'rb') as pdf_file:
                pdf_bytes = pdf_file.read()

            os.makedirs(self.output_dir, exist_ok=True)

            # Convert PDF bytes to PNG
            images = convert_from_bytes(pdf_bytes)
            for i, image in enumerate(images):
                image.save(f"{self.output_dir}/{self.output_filename_prefix}_{i + 1}.png", 'PNG')

    def run(self) -> None:
        """
        This function runs the module.
        """
        # while True: # TODO do not leave this in
        response = self.get_latex()
        self.generate_pngs(response)
        print("Done!")
            # break
