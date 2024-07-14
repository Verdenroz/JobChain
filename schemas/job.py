from typing import List, Optional

from pydantic import BaseModel, Field


class JobAgentState(BaseModel):
    query: str = Field(description="The query to search for jobs")
    jobs: Optional[List[dict]] = Field(
        default=[],
        description="The formatted list of jobs that includes job title, company name, description, and url to job posting"
    )
