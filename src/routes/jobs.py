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
        field: Optional[str] = Query(
            None,
            description="Optional field of study or expertise related to the query"),
        companies: Optional[str] = Query(
            None,
            description="Optional list of companies related to the query"),
):
    response.headers["Access-Control-Allow-Origin"] = "*"
    companies = companies.split(',') if companies else None

    agent = MasterAgent(query, field, companies)

    result = await agent.run()
    if result is None or result.get('jobs') is None:
        return {"message": "No jobs found"}

    print(result)
    return result['jobs']
