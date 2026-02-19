from pydantic import BaseModel, Field
from typing import Optional
# class for the structured output from the model and input to the resume template
class ResumeData(BaseModel):
    summary: str
    languages: str
    ml_ai: Optional[str]
    tools_frameworks: str
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

class Skills(BaseModel):
    languages: list[str]
    ml_ai: list[str]
    tools_frameworks: list[str]

class JobHistory(BaseModel):
    general_information: str
    skills: Skills
    job_history: list[JobEntry]