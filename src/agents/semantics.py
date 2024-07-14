import json

from langgraph.constants import END

from schemas.job import JobAgentState
from src.utils.model import invoke_model


class SemanticsAgent():
    def __init__(self):
        pass

    async def clarify_query(self, state: JobAgentState):
        query = state.query
        prompt = [{
            "role": "system",
            "content": "You are a expert writing professional specializing only in technical writing. Your goal is to "
                       "understand the intent and to improve the conciseness of the language.\n "
        }, {
            "role": "user",
            "content": f"Given the query: {query}\n"
                       f"Your task is to make the query more simple and concise"
                       f"The query should be related to job related topics\n"
                       f"Please provide a simplified version of the query\n"
                       f"You must return nothing but a JSON with the field 'query' (str)\n"

        }]
        response = invoke_model(prompt, 'gpt-3.5-turbo', response_format='json')
        response_json = json.loads(response)

        return {"query": response_json.get("query")}

    def get_semantics(self, state):
        query = state.query
        prompt = [{
            "role": "system",
            "content": "You are an expert in identifying topics of information based on sentences.\n "
        }, {
            "role": "user",
            "content": f"Given the query: {query}\n"
                       f"Your task is to identify if the query is relevant to job related topics\n"
                       f"If the query is relevant to job related topics, then return a simple 'YES'\n"
                       f"If the query is not relevant to job related topics, then return a simple 'NO'\n"
                       f"Job related topics include finding jobs, finding open positions, jobs with salaries, etc.\n"
                       f"Please provide a JSON object with the field 'query' (str)"

        }]
        response = invoke_model(prompt, 'gpt-4o', response_format='json')
        response_json = json.loads(response)

        result = response_json.get("query")
        if result == 'NO':
            return END
        return 'search'
