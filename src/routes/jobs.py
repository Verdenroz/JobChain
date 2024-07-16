from typing import Optional

from fastapi import APIRouter, Query, Response, Security
from fastapi.security import APIKeyHeader

from src.agents.master import MasterAgent

router = APIRouter()


@router.get("/jobs",
            summary="Returns a list of jobs",
            description="Get a list of jobs that are currently available.",
            dependencies=[Security(APIKeyHeader(name="x-api-key", auto_error=False))]
            )
async def get_jobs(
        response: Response,
        query: str = Query(
            ...,
            description="Optional query to filter jobs by title or company name"),
        source: Optional[str] = Query(
            None,
            description="Optional provider/job aggregator to filter jobs by"),
        max_results: Optional[int] = Query(
            5,
            description="Optional maximum number of jobs to return")
):
    response.headers["Access-Control-Allow-Origin"] = "*"
    sources = source.split(',') if source else None

    agent = MasterAgent(query, sources, max_results)

    result = await agent.run()
    if result is None or result.get('jobs') is None:
        return {"message": "No jobs found"}

    print(result)
    return result['jobs']
