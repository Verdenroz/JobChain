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
        query: Optional[str] = Query(
            None,
            description="Optional query to filter jobs by title or company name"),
):
    response.headers["Access-Control-Allow-Origin"] = "*"

    agent = MasterAgent(query)

    result = await agent.run()

    return result.get('jobs')
