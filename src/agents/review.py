import asyncio
import json

from langchain_community.adapters.openai import convert_openai_messages
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer
from langchain_core.exceptions import OutputParserException
from langchain_openai import ChatOpenAI

from schemas.job import Job
from src.agents.memory.job_state import JobAgentState
from src.utils.model import invoke_model


class ReviewAgent:
    def __init__(self):
        pass

    async def revise(self, state: JobAgentState):
        """
        Checks if jobs should be revised if there are no jobs scraped
        :param state:
        :return: True if jobs should be revised
        """
        revisions = state.get('revisions') if state.get('revisions') else 1
        if revisions >= state.get('max_revisions'):
            return 'END'

        jobs = state.get('jobs') if state.get('jobs') else []
        if not jobs or len(jobs) == 0:
            return True

        return False

    async def revise_query(self, state: JobAgentState):
        """
        Revises the query if there are no jobs scraped
        :param state:
        """
        query = state.get('query')
        revisions = state.get('revisions') if state.get('revisions') else 1
        prompt = [{
            "role": "system",
            "content": "You are an expert in simplifying complicated queries.\n "
        }, {
            "role": "user",
            "content": f"Given the query : {query}.\n"
                       f"Your task is to simplify the query and make it even more concise\n"
                       f"If there are multiple companies, you can simplify the query by focusing on one company\n"
                       f"Please return  as a json with the field 'query' (str) and the simplified query as the value \n"
        }]
        response = invoke_model(prompt, 'gpt-3.5-turbo', response_format='json')
        response_json = json.loads(response)

        return {
            "query": response_json.get('query'),
            "revisions": revisions + 1,
        }

    async def review(self, state: JobAgentState):
        """
        Reviews jobs with more than 3 missing fields, updating them with new fields if possible
        :param state:
        :return:
        """
        jobs = state['jobs']
        jobs_to_review = []

        # Filter Jobs
        for job in jobs:
            fields_to_check = ['job_description', 'job_location', 'job_posted_date', 'job_type', 'job_salary']
            missing_fields = sum(1 for field in fields_to_check if getattr(job, field, 'Unknown') in ['Unknown', None])

            if missing_fields > 3:
                jobs_to_review.append(job)

        # Review in Parallel
        review_tasks = [self.review_job(job) for job in jobs_to_review]
        reviewed_jobs = await asyncio.gather(*review_tasks)

        # Update Jobs List
        for job in reviewed_jobs:
            if job is None:
                continue
            index = jobs.index(job)
            jobs[index] = job

        return {"jobs": jobs}

    async def review_job(self, job):
        """
        Review a single job
        :param job:
        :return:
        """
        print(f"Reviewing job: {job}")
        url = str(job.url)
        # Load the urls into Documents
        loader = AsyncHtmlLoader(web_path=url)
        try:
            doc = loader.load()
        except Exception as e:
            print(f"Error loading document: {e}")
            return None

        # Try text transformer instead
        html2text = Html2TextTransformer()
        doc_transformed = html2text.transform_documents(doc)

        text = doc_transformed[0].page_content[4000:6000]
        prompt = [{
            "role": "system",
            "content": "You are an expert in extracting job postings from website text content.\n "
        }, {
            "role": "user",
            "content": f"Given the text content of a job posting : {text}\n"
                       f" your task is to extract relevant information related to the posting\n"
                       f"Required information includes the job title, company name\n"
                       f"Optional information includes the job description, job location, job salary, date posted, job type, and url\n"
        }]
        lc_messages = convert_openai_messages(prompt)

        try:
            llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0).with_structured_output(schema=Job)
            job_dict = await llm.ainvoke(lc_messages)
            # Update the original job with new fields from job_dict
            job_dict = dict(job_dict)
            job_dict.update(job)
            print(f"Updated job: {job_dict}")
            return job_dict
        except OutputParserException:
            return job
