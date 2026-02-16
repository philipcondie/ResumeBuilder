from jinja2 import Environment, FileSystemLoader

from config import TEMPLATES_DIR
from models import JobHistory

class PromptGenerator:
    def __init__(self, prompt_template_filename, experience_filepath, description_filepath):
        self.prompt_template_file = prompt_template_filename
        self.experience_file = experience_filepath
        self.description_file = description_filepath

        self.jinja_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
        self.jinja_template = self.jinja_env.get_template(prompt_template_filename)

    def generate_prompt(self):
        # load file contents
        try:
            with open(self.experience_file, mode='r', encoding='utf-8') as exp_file:
                contents = exp_file.read()
            job_history = JobHistory.model_validate_json(contents)

            with open(self.description_file, mode='r', encoding='utf-8') as desc_file:
                job_description = desc_file.read()
        except FileNotFoundError:
            print(f"Error: The file '{self.experience_file}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}") 
        data = {
            **job_history.model_dump(),
            "job_description": job_description
        }
        # render template
        return self.jinja_template.render(**data)