import os

from tavily import TavilyClient

from src.agents.job_state import JobAgentState

aggregators = [
    'https://www.indeed.com/',
    'https://www.monster.com/',
    'https://www.linkedin.com/',
    'https://www.ziprecruiter.com/',
    'https://www.glassdoor.com/',
    'https://www.dice.com/',
]
class SearchAgent:
    def __init__(self):
        pass

    async def find_job_urls(self, state: JobAgentState):
        query = state['query']
        print(query)

        client = TavilyClient(os.environ.get('TAVILY_API_KEY'))

        jobs_info = client.search(query, max_results=5, exclude_domains=aggregators)['results']
        print(jobs_info)

        urls = [job['url'] for job in jobs_info]
        print(urls)

        return {"urls": urls}


