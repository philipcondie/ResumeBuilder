from render import Render
from llm import LLM
from prompt import Prompt
from config import DATA_DIR, TEMPLATES_DIR, OUTPUT_DIR

prompt = Prompt(
    prompt_template_filename="prompt.j2",
    experience_path= DATA_DIR / "sample.json",
    description_path= DATA_DIR / "jobs/test.txt"
)

prompt = prompt.generate_prompt()

llm = LLM()
output = llm.send_message(prompt)

renderer = Render(
    template_dir=TEMPLATES_DIR,
    template_filename="base_template.html",
    output_dir=OUTPUT_DIR,
    output_filename="test_1"
)

renderer.generate_resume(output)