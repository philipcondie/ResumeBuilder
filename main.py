from render import Render
from llm import LLM
from prompt import Prompt
from config import DATA_DIR, TEMPLATES_DIR, OUTPUT_DIR

# prompt = Prompt(
#     prompt_template_filename="prompt.j2",
#     experience_path= DATA_DIR / "sample.json",
#     description_path= DATA_DIR / "jobs/test.txt",
#     system_prompt_path= TEMPLATES_DIR / "system_prompt.md"
# )

# user_message = prompt.generate_prompt()
# system_prompt = prompt.get_system_prompt()

# llm = LLM(system_prompt)
# output = llm.send_message(user_message)

renderer = Render(
    template_dir=TEMPLATES_DIR,
    template_filename="base_template.html",
    output_dir=OUTPUT_DIR,
    output_filename="clearstory_3"
)

# renderer.generate_resume(output)
renderer.rerender_pdf(dir=OUTPUT_DIR,filename="clearstory")