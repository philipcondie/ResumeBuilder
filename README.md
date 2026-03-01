# ResumeBuilder

An AI-powered CLI tool that generates tailored resumes for job applications. Given a job description, it uses Claude to rewrite your experience bullets, craft a targeted summary, and reorder your skills — then outputs a polished HTML and PDF resume.

## How It Works

1. Provide a job description (file or clipboard)
2. Claude analyzes the role against your job history and skills
3. A tailored resume is rendered to HTML and PDF

## Setup

**Prerequisites:** Python 3.13+, an Anthropic API key

```bash
# Clone and enter the project
git clone <repo-url> && cd ResumeBuilder

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Add your API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

## Usage

```bash
python main.py <job_name>
```

This looks for a job description at `data/jobs/<job_name>.txt` and outputs `output/<job_name>.html` and `output/<job_name>.pdf`.

**Options:**

| Flag | Description |
|------|-------------|
| `--jd-file <path>` | Use an alternate job description file |
| `--pdf-only` | Re-render PDF from an existing HTML file |

**Examples:**

```bash
# Generate resume for a saved job description
python main.py acme_widget_maker

# Use a one-off job description file
python main.py my_application --jd-file ~/Downloads/google_jd.txt

# Regenerate PDF from existing HTML (no API call)
python main.py acme_widget_maker --pdf-only
```

If no job description file is found, you'll be prompted to paste the job description directly into the terminal.

## Project Structure

```
ResumeBuilder/
├── main.py          # CLI entry point
├── llm.py           # Claude API integration
├── prompt.py        # Jinja2 prompt construction
├── render.py        # HTML + PDF generation via Playwright
├── models.py        # Pydantic data models
├── config.py        # Path configuration
├── data/
│   ├── job_history.json    # Your work experience and skills
│   └── jobs/               # Job description text files
├── templates/
│   ├── base_template.html  # Resume HTML template
│   ├── prompt.j2           # LLM prompt template
│   └── system_prompt.md    # Claude system instructions
└── output/                 # Generated resumes (HTML + PDF)
```

## Customizing Your Data

See [CUSTOMIZATION.md](CUSTOMIZATION.md) for a full guide on editing your job history, tagging experience bullets, and modifying the resume HTML template.

The two key files are:
- **`data/job_history.json`** — your master resume data (experience, skills, context for Claude)
- **`templates/base_template.html`** — the Jinja2 template that controls layout and styling

## Dependencies

- [anthropic](https://github.com/anthropics/anthropic-sdk-python) — Claude API client
- [pydantic](https://docs.pydantic.dev/) — Structured output validation
- [jinja2](https://jinja.palletsprojects.com/) — Template rendering
- [playwright](https://playwright.dev/python/) — PDF generation via headless Chromium
- [python-dotenv](https://github.com/theskumar/python-dotenv) — Environment variable management
