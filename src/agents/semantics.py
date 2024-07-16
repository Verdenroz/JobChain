import json

from src.agents.memory.job_state import JobAgentState
from src.utils.model import invoke_model


class SemanticsAgent:
    def __init__(self):
        pass

    async def clarify_query(self, state: JobAgentState):
        """
        Given a query, the agent will simplify the query and incorporate companies and fields related to the query.
        :param state:
        :return:
        """
        initial_query = state['initial_query']

        prompt = [{
            "role": "system",
            "content": "You are a expert writing professional specializing only in technical writing. Your goal is to "
                       "understand the intent and to improve the conciseness of the language.\n "
        }, {
            "role": "user",
            "content": f"Given the query: {initial_query}\n"
                       f"Your task is to make the query more simple and concise and have it relate to job related topics\n"
                       f"The query should be related to job related topics\n"
                       f"Please provide a simplified version of the query\n"
                       f"You must return nothing but a JSON with the field 'query' (str)\n"

        }]
        response = invoke_model(prompt, 'gpt-3.5-turbo', response_format='json')
        response_json = json.loads(response)

        return {"query": response_json.get("query")}

    @staticmethod
    def passes_semantics(state):
        """
        Given a query, the agent will determine if the query is related to job topics.
        If the query is related to job topics, then the agent will return True else False.
        :param state:
        :return:
        """
        initial_query = state['initial_query']
        prompt = [{
            "role": "system",
            "content": "You are an expert in identifying topics of information based on sentences.\n "
        }, {
            "role": "user",
            "content": f"Given the query: {initial_query}\n"
                       f"Your task is to identify if the query is relevant to job related topics\n"
                       f"If the query is relevant to job related topics, then return a simple 'YES'\n"
                       f"If the query is not relevant to job related topics, then return a simple 'NO'\n"
                       f"Job related topics include finding jobs, finding open positions, jobs with salaries, etc.\n"
                       f"Examples of non-job related topics include: 'What is the capital of France?', 'What is the weather today?', math questions.\n"
                       f"Any query that is not a topic related to jobs should return 'NO'\n"
                       f"Please provide a JSON object with the field 'query' (str)"

        }]
        response = invoke_model(prompt, 'gpt-4o', response_format='json')
        response_json = json.loads(response)

        result = response_json.get("query")
        return result == 'YES'
