from typing import List, Optional, TypedDict


class JobAgentState(TypedDict):
    initial_query: str
    max_results: int
    query: str
    sources: Optional[List[str]]
    urls: Optional[List[str]]
    job_listings: Optional[List[dict]]
    jobs: Optional[List[dict]]
    max_revisions: int
    revisions: int
