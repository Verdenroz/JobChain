import os

from tavily import TavilyClient

from src.agents.memory.job_state import JobAgentState


class SearchAgent:
    def __init__(self, providers: list[str]):
        self.providers = providers
        pass

    async def find_job_urls(self, state: JobAgentState):
        """
        Find job urls based on a query
        :param state:
        :return:
        """
        query = state['query']
        sources = state.get('sources') if state.get('sources') else self.providers

        client = TavilyClient(os.environ.get('TAVILY_API_KEY'))

        jobs_info = client.search(query, max_results=2, include_domains=sources)['results']

        urls = [job['url'] for job in jobs_info]
        return {"urls": urls}
