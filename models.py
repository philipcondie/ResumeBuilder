from pydantic import BaseModel

# class for the structured output from the model and input to the resume template
class ResumeData(BaseModel):
    addsalt: list[str]
    chevron_tech_service: list[str]
    chevron_process_design: list[str]
    valero: list[str]

# classes for job experience
class ExperienceItem(BaseModel):
    text: str
    tags: list[str]
    category: str

class JobEntry(BaseModel):
    company: str
    job_title: str
    start_date: str
    end_date: str
    experience_items: list[ExperienceItem]

class JobHistory(BaseModel):
    job_history: list[JobEntry]