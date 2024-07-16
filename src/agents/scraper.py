import asyncio

from langchain_community.adapters.openai import convert_openai_messages
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer
from langchain_core.exceptions import OutputParserException
from langchain_openai import ChatOpenAI

from schemas.job import Job
from src.agents.job_state import JobAgentState


class ScraperAgent:
    def __init__(self):
        pass

    async def scrape_html(self, state: JobAgentState):
        urls = state['urls']
        jobs = state.get('jobs') if state.get('jobs') else []

        # Load the urls into Documents
        loader = AsyncHtmlLoader(urls)
        docs = loader.load()

        # Transform the html content into text
        html2text = Html2TextTransformer()
        docs_transformed = html2text.transform_documents(docs)

        # Process each document in parallel
        tasks = [self.process_document(doc, urls[i]) for i, doc in enumerate(docs_transformed)]
        jobs_results = await asyncio.gather(*tasks)

        # Filter out None results and extend the jobs list
        jobs.extend([job for job in jobs_results if job is not None])

        return {"jobs": jobs}

    async def process_document(self, doc, url):
        text = doc.page_content[2000:4000]
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
            job_with_url = dict(job_dict)
            job_with_url['url'] = url
            return job_with_url
        except OutputParserException:
            return None
