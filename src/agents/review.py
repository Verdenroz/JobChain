import asyncio

from langchain_community.adapters.openai import convert_openai_messages
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer
from langchain_core.exceptions import OutputParserException
from langchain_openai import ChatOpenAI

from schemas.job import Job


class ReviewAgent:
    def __init__(self):
        pass

    async def revise(self, state):
        jobs = state['jobs']
        if not jobs or len(jobs) == 0:
            return True

        return False

    async def review(self, state):
        jobs = state['jobs']
        jobs_to_review = []

        # Step 1: Filter Jobs
        for job in jobs:
            fields_to_check = ['job_description', 'job_location', 'job_posted_date', 'job_type', 'job_salary']
            missing_fields = sum(1 for field in fields_to_check if not job.get(field))
            if missing_fields > 3:
                jobs_to_review.append(job)

        # Step 2: Review in Parallel
        review_tasks = [self.review_job(job) for job in jobs_to_review]
        reviewed_jobs = await asyncio.gather(*review_tasks)

        # Step 3: Update Jobs List
        for job in reviewed_jobs:
            index = jobs.index(job)
            jobs[index] = job

        return {"jobs": jobs}

    async def review_job(self, job):
        print(f"Reviewing job: {job}")
        url = job['url']
        # Load the urls into Documents
        loader = AsyncHtmlLoader(url)
        doc = loader.load()

        # Transform the html content into text
        html2text = Html2TextTransformer()
        doc_transformed = html2text.transform_documents(doc)

        # Shifts text downwards for potential new content
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
