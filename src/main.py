import asyncio

from dotenv import load_dotenv
from fastapi import FastAPI
from mangum import Mangum

from src.agents.master import MasterAgent
from src.routes import jobs_router

# Load environment variables
load_dotenv()
app = FastAPI()

app.include_router(jobs_router)

handler = Mangum(app)


async def main():
    query = "Find me Software Engineering jobs"
    chief_editor = MasterAgent(query)
    jobs = await chief_editor.stream()

    return jobs

if __name__ == "__main__":
    asyncio.run(main())