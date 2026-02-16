from render import Render
from llm import LLM
from pathlib import Path
from prompt import PromptGenerator
from config import DATA_DIR, TEMPLATES_DIR, OUTPUT_DIR

generator = PromptGenerator(
    prompt_template_filename="prompt.j2",
    experience_filepath= DATA_DIR / "sample.json",
    description_filepath=DATA_DIR / "jobs/test.txt"
)

prompt = generator.generate_prompt()

llm = LLM()
output = llm.send_message(prompt)

renderer = Render(
    template_dir=TEMPLATES_DIR,
    template_file="base_template.html",
    output_dir=str(OUTPUT_DIR),
    output_filename="test_1"
)

renderer.generate_resume(output)