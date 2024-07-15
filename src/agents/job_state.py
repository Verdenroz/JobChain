from typing import List, Optional, TypedDict


class JobAgentState(TypedDict):
    initial_query: str
    query: str
    companies: Optional[List[str]]
    field: Optional[str]
    urls: Optional[List[str]]
    jobs: Optional[List[dict]]
