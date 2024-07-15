from typing import Optional

from langchain_core.pydantic_v1 import BaseModel, Field


class Job(BaseModel):
    job_title: str = Field(description="The title of the job")
    job_company: str = Field(description="The company offering the job")
    job_description: Optional[str] = Field(description="The description of the job")
    job_location: Optional[str] = Field(description="The location of the job")
    job_posted_date: Optional[str] = Field(description="The date the job was posted")
    job_type: Optional[str] = Field(description="The type of job (e.g., full-time, part-time)")
    job_salary: Optional[str] = Field(description="The salary for the job")
    url: Optional[str] = Field(description="The URL of the job posting")
