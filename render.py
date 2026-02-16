from playwright.sync_api import sync_playwright
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import datetime

BASE_DIR = Path(__file__).resolve().parent / "output"

class Render:
    def __init__(self, template_dir, template_file, output_dir = None, output_filename = None):
        # set up jinja
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))
        self.jinja_template = self.jinja_env.get_template(template_file)

        # set up file management (html, pdf)
        self.output_dir = Path(output_dir) if output_dir else BASE_DIR
        self.output_filename = output_filename if output_filename else ( "resume_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        self.html_filename = self.output_dir / f"{self.output_filename}.html"
        self.pdf_filename = self.output_dir / f"{self.output_filename}.pdf"

    def to_html(self, data):
        html = self.jinja_template.render(**data)
        try:
            with open(file=self.html_filename, mode='w') as file:
                file.write(html)
        except Exception as e:
            print(f"An error occured: {e}")

    def to_pdf(self):
        try:
            with open(file=self.html_filename, mode='r', encoding='utf-8') as file:
                html_string = file.read()
            
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.set_content(html_string)
                page.pdf(path=self.pdf_filename,format="Letter")
                browser.close()

        except FileNotFoundError:
            print(f"Error: The file '{self.html_filename}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def generate_resume(self, data):
        self.to_html(data)
        self.to_pdf()