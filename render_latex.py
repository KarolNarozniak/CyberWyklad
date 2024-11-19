import subprocess
import os

def generate_png_from_latex(latex_file):
    # Ścieżka do Pulpitu użytkownika
    desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    
    # Nazwa pliku PNG wynikowego
    output_png = os.path.join(desktop_path, 'out.png')

    # Sprawdzamy, czy plik LaTeX istnieje
    if not os.path.isfile(latex_file):
        print(f"Plik {latex_file} nie istnieje.")
        return

    # Kompilacja pliku LaTeX do PDF
    try:
        subprocess.run(['pdflatex', latex_file], check=True)
        print(f"Plik PDF {latex_file} został pomyślnie wygenerowany.")
    except subprocess.CalledProcessError:
        print("Błąd podczas kompilacji LaTeX.")
        return

    # Zmieniamy nazwę pliku PDF na nazwę wynikową PNG
    pdf_file = latex_file.replace('.tex', '.pdf')

    # Konwersja PDF do PNG za pomocą pdftoppm (poppler-utils)
    try:
        subprocess.run(['pdftoppm', '-png', pdf_file, os.path.join(desktop_path, 'out')], check=True)
        print(f"Plik PNG został wygenerowany: {output_png}")
    except subprocess.CalledProcessError:
        print("Błąd podczas konwersji PDF do PNG.")
        return

    # Czyszczenie plików pośrednich (pliki PDF i AUX)
    for ext in ['.pdf', '.aux', '.log']:
        os.remove(latex_file.replace('.tex', ext))
    print("Pliki pośrednie zostały usunięte.")

# Przykład użycia:
latex_file = r'C:\Users\Preze\Desktop\kod.tex'  # Ścieżka do pliku LaTeX na Pulpicie
generate_png_from_latex(latex_file)
