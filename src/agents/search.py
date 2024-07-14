import json
import os

from langchain_community.adapters.openai import convert_openai_messages
from tavily import TavilyClient

from schemas.job import JobAgentState
from src.utils.model import invoke_model


class SearchAgent:
    def __init__(self):
        pass

    async def find_jobs(self, state: JobAgentState):
        query = state.query

        client = TavilyClient(os.environ.get('TAVILY_API_KEY'))

        jobs_info = client.search(query, search_depth='advanced')['results']

        prompt = [{
            "role": "system",
            "content": f'You are an AI critical thinker research assistant. '
                       f'Your sole purpose is to write well written, critically acclaimed,'
                       f'objective and structured reports on given text.'
        }, {
            "role": "user",
            "content":  f'Information: """{jobs_info}"""\n\n'
                        f'query: "{query}" in a detailed summary --'
                        f'Using the above information, separate and format each job posting, adhering to the query'
                        f'Ensure that the job title, company name, description, and url to job posting are included in the response'
                        f'Please provide a JSON object with the field "jobs" (List[dict])'
        }]

        response = invoke_model(prompt, model='gpt-3.5-turbo', response_format='json')
        response_json = json.loads(response)

        return {"jobs": response_json.get("jobs")}
