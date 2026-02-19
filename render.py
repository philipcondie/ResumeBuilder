from playwright.sync_api import sync_playwright
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import datetime

BASE_DIR = Path(__file__).resolve().parent / "output"

def get_filename_counter(directory: Path, filename: str):
    stem = Path(filename).stem
    suffix = Path(filename).suffix
    candidate_path = directory / filename
    counter = 0
    while candidate_path.exists():
        candidate_path = directory / f"{stem}_{counter}{suffix}"
        counter += 1

    return counter

class Render:
    def __init__(self, 
                template_dir: Path,
                template_filename: str,
                output_dir: Path | None = None,
                output_filename: str | None = None
            ):
        # set up jinja
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))
        self.jinja_template = self.jinja_env.get_template(template_filename)

        # set up file management (html, pdf)
        self.output_dir = Path(output_dir) if output_dir else BASE_DIR
        self.output_filename = output_filename or ( "resume_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        if output_filename:
            # check for if the pdf or html extension has the higher file counter
            html_counter = get_filename_counter(self.output_dir, f"{output_filename}.html")
            pdf_counter = get_filename_counter(self.output_dir, f"{output_filename}.pdf")
            file_counter = max(html_counter, pdf_counter)
            self.output_filename = f"{output_filename}_{file_counter}" if file_counter else output_filename
        else:
            self.output_filename = "resume_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
        self.html_path = self.output_dir / f"{self.output_filename}.html"
        self.pdf_path = self.output_dir / f"{self.output_filename}.pdf"

    def to_html(self, data):
        html = self.jinja_template.render(**data)
        try:
            with open(file=self.html_path, mode='w') as file:
                file.write(html)
        except Exception as e:
            print(f"An error occured: {e}")

    def to_pdf(self):
        try:
            with open(file=self.html_path, mode='r', encoding='utf-8') as file:
                html_string = file.read()
            
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.set_content(html_string)
                page.pdf(path=self.pdf_path,format="Letter")
                browser.close()

        except FileNotFoundError:
            print(f"Error: The file '{self.html_path}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def generate_resume(self, data):
        self.to_html(data)
        self.to_pdf()