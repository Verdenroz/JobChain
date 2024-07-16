import json

from src.agents.job_state import JobAgentState
from src.utils.model import invoke_model


class SemanticsAgent:
    def __init__(self):
        pass

    async def clarify_query(self, state: JobAgentState):
        companies = state.get('companies') if state.get('companies') else await self.find_default_companies(state)
        field = state.get('field') if state.get('field') else await self.find_default_field(state)
        initial_query = state['initial_query']

        prompt = [{
            "role": "system",
            "content": "You are a expert writing professional specializing only in technical writing. Your goal is to "
                       "understand the intent and to improve the conciseness of the language.\n "
        }, {
            "role": "user",
            "content": f"Given the query: {initial_query}\n"
                       f"Your task is to make the query more simple and concise and have it relate to job related topics\n"
                       f'The query should be related to "{field}" at "{companies}"\n'
                       f"The query should be related to job related topics\n"
                       f"Please provide a simplified version of the query\n"
                       f"You must return nothing but a JSON with the field 'query' (str)\n"

        }]
        response = invoke_model(prompt, 'gpt-3.5-turbo', response_format='json')
        response_json = json.loads(response)

        return {"query": response_json.get("query")}

    @staticmethod
    def passes_semantics(state):
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

    async def find_default_field(self, state: JobAgentState):
        query = state['initial_query']
        prompt = [{
            "role": "system",
            "content": f'You are a knowledgeable expert in the identifying fields of studies and expertise.'
        }, {
            "role": "user",
            "content": f'query: "{query}"'
                       f'Using the above query, identify the field of study/expertise related to the query.'
                       f'If the query does not have an obvious field, then return the closest you can think of.'
                       f'Example fields include: "Data Science", "Marketing", "Software Engineering", etc.'
                       f'Please return a json object with the key "field" (str) and the field name as the value.'
        }]
        response = invoke_model(prompt, model='gpt-4o', response_format='json')
        response_json = json.loads(response)
        field = response_json.get("field")

        if field is None or len(field) == 0:
            field = ""
        return field

    async def find_default_companies(self, state: JobAgentState):
        query = state['query']
        prompt = [{
            "role": "system",
            "content": f'You are an expert in identifying companies that are hiring.'
        }, {
            "role": "user",
            "content": f'query: "{query}"'
                       f'Using the above query, identify companies related to the query.'
                       f'If the query does not specifically have a company name, then return a list of default companies.'
                       f'Default companies are prominent companies closely related to the query.'
                       f'Example companies include: "Google", "Facebook", "Amazon", etc.'
                       f'Please return a json object with the key "companies" and a list of companies as the value.'
        }]
        response = invoke_model(prompt, model='gpt-4o', response_format='json')
        response_json = json.loads(response)
        companies = response_json.get("companies")

        if companies is None or len(companies) == 0:
            companies = ""

        return companies
