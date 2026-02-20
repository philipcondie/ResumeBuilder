import argparse
import subprocess
import sys

from render import Render
from llm import LLM
from prompt import Prompt
from config import DATA_DIR, TEMPLATES_DIR, OUTPUT_DIR

def get_clipboard():
    # macOS
    result = subprocess.run(['pbpaste'], capture_output=True, text=True)
    return result.stdout.strip()

def main():
    parser = argparse.ArgumentParser(description="CLI for generating custom tailored resumes")
    parser.add_argument("job_name", help='Job identifier (e.g. acme_corp_swe)') # used for output filenames
    parser.add_argument("--jd-file", help="Name of existing job description file")
    args = parser.parse_args()

    # create jd file path
    jd_path = DATA_DIR / "jobs" / f"{args.job_name}.txt"


    # check for existing jd file 
    if args.jd_file:
        if (DATA_DIR / "jobs" / args.jd_file).exists():
            prompt = Prompt(
                prompt_template_filename="prompt.j2",
                experience_path= DATA_DIR / "sample.json",
                description_path= DATA_DIR / "jobs" / args.jd_file,
                system_prompt_path= TEMPLATES_DIR / "system_prompt.md"
            )
    elif jd_path.exists():
        print(f'Found existing JD at {jd_path}, using it.')
        prompt =  Prompt(
            prompt_template_filename="prompt.j2",
            experience_path= DATA_DIR / "sample.json",
            description_path= jd_path,
            system_prompt_path= TEMPLATES_DIR / "system_prompt.md"
        )
    else:
        jd_text = get_clipboard()
        if not jd_text:
            print('Error: clipboard is empty and no JD file found.')
            sys.exit(1)
        jd_path.write_text(jd_text)
        print(f'Saved JD to {jd_path}')
        prompt =  Prompt(
            prompt_template_filename="prompt.j2",
            experience_path= DATA_DIR / "sample.json",
            description_path= jd_path,
            system_prompt_path= TEMPLATES_DIR / "system_prompt.md"
        )

    llm = LLM(prompt.get_system_prompt())
    output = llm.send_message(prompt.generate_prompt())
    renderer = Render(
        template_dir=TEMPLATES_DIR,
        template_filename="base_template.html",
        output_dir=OUTPUT_DIR,
        output_filename=args.job_name
    )

    renderer.generate_resume(output)

if __name__ == "__main__":
    main()