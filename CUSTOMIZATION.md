# Customization Guide

This guide covers the two files you'll edit most when adapting ResumeBuilder for yourself: your job history data and the HTML resume template.

---

## Job History (`data/job_history.json`)

This is your master resume — the full source of truth that Claude draws from when tailoring each application. Claude reads this file and selects, rewrites, and reorders content to fit the target job description.

### Top-Level Structure

```json
{
  "general_information": "...",
  "skills": { ... },
  "job_history": [ ... ]
}
```

---

### `general_information`

A plain-English paragraph describing your background, career transition, and targeting intent. Claude uses this as context when deciding how to frame your experience.

```json
"general_information": "Candidate is looking to break into the widget making business..."
```

**Tips:**
- Be explicit about what roles you're targeting (e.g. "backend", "full-stack", "ML engineering")
- Mention any relevant context that isn't obvious from your job titles (degrees in progress, part-time work, etc.)
- This doesn't appear on the resume — it's purely for Claude's reasoning

---

### `skills`

Three lists of skills. Claude reorders these by relevance to the job description before rendering.

```json
"skills": {
  "languages": ["WidgetScript", "CogML", "AssemblyPlus"],
  "ml_ai": ["WidgetNet", "CogLearn", "AutoGadget"],
  "tools_frameworks": ["GadgetUI", "BoltDB", "WidgetDock", "FastCrank"]
}
```

| Field | What it maps to on the resume |
|-------|-------------------------------|
| `languages` | **Languages:** line in Technical Skills |
| `ml_ai` | **ML / AI:** line — conditionally shown (see template section) |
| `tools_frameworks` | **Tools/Frameworks:** line |

**Tips:**
- Only include skills you can speak to in an interview
- `ml_ai` is the only optional section — it's hidden when the role isn't ML-relevant (controlled by the `{% if ml_ai %}` check in the template)

---

### `job_history`

An array of job entries, each with a list of experience items.

```json
{
  "company": "Acme Widget Co.",
  "job_title": "Senior Widget Engineer",
  "start_date": "January 2023",
  "end_date": "Present",
  "experience_items": [ ... ]
}
```

#### Experience Items

Each item has three fields:

```json
{
  "text": "Redesigned the widget assembly pipeline, reducing average crank time by 40% across 3 production lines.",
  "tags": ["optimization", "manufacturing", "process-improvement", "quantified"],
  "category": "accomplishment-quantified"
}
```

| Field | Purpose |
|-------|---------|
| `text` | The raw bullet. Claude rewrites this using job-aligned language — write it clearly but don't over-polish it |
| `tags` | Keywords Claude uses to match bullets to job requirements. More specific tags = better selection |
| `category` | A grouping label for your own organization. Not used directly by Claude but helps you audit coverage |

**Tips:**
- Include more bullets than you'd ever put on a resume — Claude selects the most relevant subset
- Tags are the primary signal for bullet selection. Tag each bullet with the skills and themes it demonstrates (e.g. `"system-design"`, `"client-facing"`, `"debugging"`, `"leadership"`)
- Write bullet `text` in past tense with a strong action verb and a concrete result where possible

#### Common Tag Conventions (Examples)

| Tag | Meaning |
|-----|---------|
| `design`, `manufacturing`, `quality-control` | Domain area |
| `optimization`, `process-improvement` | Efficiency-focused work |
| `system-design`, `architecture` | Design-level contributions |
| `leadership`, `team-management` | People/project ownership |
| `client-facing` | External stakeholder interaction |
| `accomplishment-quantified` | Has a dollar/number/percentage metric |
| `debugging`, `troubleshooting` | Problem-solving focus |

You can define your own tags — just be consistent so Claude can reason about them.

---

## Resume Template (`templates/base_template.html`)

This is a Jinja2 HTML template. The rendered output is saved to `output/` as both `.html` and `.pdf`.

### Variables Injected by Claude

These placeholders are filled in by `ResumeData` — the structured output Claude returns:

| Variable | Type | Description |
|----------|------|-------------|
| `{{ summary }}` | string | 2–3 sentence tailored summary |
| `{{ languages }}` | string | Comma-separated, reordered by relevance |
| `{{ ml_ai }}` | string or None | Hidden if None/empty |
| `{{ tools_frameworks }}` | string | Comma-separated, reordered by relevance |
| `{{ acme_widget_co }}` | list | Selected/rewritten bullets for Acme Widget Co. role |
| `{{ gadget_corp_senior }}` | list | Bullets for Gadget Corp Senior role |
| `{{ gadget_corp_junior }}` | list | Bullets for Gadget Corp Junior role |
| `{{ proto_labs }}` | list | Bullets for Proto Labs role |

Bullet lists are rendered with:
```html
{% for bullet in acme_widget_co %}
<li>{{ bullet }}</li>
{% endfor %}
```

### Conditional Sections

The ML/AI skills line and the ML coursework line in Education are conditionally rendered:

```html
{% if ml_ai %}
<div class="skill-line">ML / AI: {{ ml_ai }}</div>
{% endif %}
```

When Claude determines the role isn't ML-focused, it returns `ml_ai: null` and both blocks are hidden automatically.

### Styling

Colors, fonts, and spacing are controlled via CSS variables at the top of the `<style>` block:

```css
:root {
  --color-text: #323232;
  --color-text-name: #1A5C71;
  --color-accent: #2a7f9e;
  --font-main: 'Open Sans', 'Helvetica Neue', Arial, sans-serif;
}
```

Change `--color-accent` and `--color-text-name` to restyle all headers, section titles, and links at once.

### Hardcoded Fields

The following are hardcoded directly in the HTML and need to be edited manually to personalize the template:

- **Name** (`<h1>Jane Widget</h1>`)
- **Phone and email** (in `.contact-info`)
- **Job title lines** (e.g. `"Senior Widget Engineer — Acme Widget Co. — Remote"`)
- **Date ranges** for each job
- **Education entries** (schools, degrees, coursework)

> If you add or remove jobs from `job_history.json`, you'll also need to update the corresponding job sections in `base_template.html` and add matching fields to the `ResumeData` model in `models.py`.

### Adding a New Job

To add a new job to the resume:

1. **`data/job_history.json`** — Add a new entry to the `job_history` array
2. **`models.py`** — Add a new `list[str]` field to `ResumeData` (e.g. `new_company: list[str]`)
3. **`templates/base_template.html`** — Add a new `<div class="job">` block with `{% for bullet in new_company %}`
4. **`templates/system_prompt.md`** — Update the system prompt so Claude knows about the new role and its corresponding output field
