from jinja2 import Environment, FileSystemLoader
from pathlib import Path

from config import TEMPLATES_DIR
from models import JobHistory

class Prompt:
    def __init__(self,
                prompt_template_filename: str,
                experience_path: Path,
                description_path: Path,
                system_prompt_path: Path
            ):
        self.prompt_template_file = prompt_template_filename
        self.experience_path= experience_path
        self.description_path = description_path
        self.system_prompt_path = system_prompt_path

        self.jinja_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
        self.jinja_template = self.jinja_env.get_template(prompt_template_filename)

    def generate_prompt(self):
        # load file contents
        try:
            with open(self.experience_path, mode='r', encoding='utf-8') as exp_file:
                contents = exp_file.read()
            job_history = JobHistory.model_validate_json(contents)

            with open(self.description_path, mode='r', encoding='utf-8') as desc_file:
                job_description = desc_file.read()
        except FileNotFoundError:
            print(f"Error: The file '{self.experience_path}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}") 
        data = {
            **job_history.model_dump(),
            "job_description": job_description
        }
        # render template
        return self.jinja_template.render(**data)
    
    def get_system_prompt(self):
        try:
            with open(self.system_prompt_path, mode='r', encoding='utf-8') as sys_file:
                return sys_file.read()
        except FileNotFoundError:
            print(f"Error: The file '{self.system_prompt_path}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")