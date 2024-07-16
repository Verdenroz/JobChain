from typing import Optional, List

from langchain_core.pydantic_v1 import BaseModel, Field


class JobListing(BaseModel):
    job_id: List[int] = Field(description="The unique identifier for the job")
    job_title: List[str] = Field(description="The title of the job")
    job_company: List[str] = Field(description="The company offering the job")
    job_description: Optional[List[str]] = Field(description="The description of the job")
    job_location: Optional[List[str]] = Field(description="The location of the job")
    job_posted_date: Optional[List[str]] = Field(description="The date the job was posted")
    job_type: Optional[List[str]] = Field(description="The type of job (e.g., full-time, part-time)")
    job_salary: Optional[List[str]] = Field(description="The salary for the job")
    urls: Optional[List[str]] = Field(description="The URLs of the job posting")
