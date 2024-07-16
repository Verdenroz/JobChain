import asyncio

from langchain_community.adapters.openai import convert_openai_messages
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_openai import ChatOpenAI

from schemas.joblisting import JobListing
from src.agents.memory.job_state import JobAgentState


class ScraperAgent:
    def __init__(self):
        pass

    async def scrape_html(self, state: JobAgentState):
        """
        Scrape the html content of the urls
        :param state:
        :return:
        """
        urls = state['urls']
        jobs = state.get('jobs') if state.get('jobs') else []

        # Load the urls into Documents
        loader = AsyncHtmlLoader(urls)
        docs = loader.load()

        # Transform the html content into text
        bs_transformer = BeautifulSoupTransformer()
        docs_transformed = bs_transformer.transform_documents(
            documents=docs,
            tags_to_extract=['h1', 'span', 'article', 'li', 'ul',  'a',  'div'],
            remove_comments=True,
            remove_lines=True,
        )

        # Process each document in parallel
        tasks = [self.process_document(doc) for doc in docs_transformed]
        jobs_results = await asyncio.gather(*tasks)

        # Filter out None results and extend the jobs list
        jobs.extend([job for job in jobs_results if job is not None])

        return {"job_listings": jobs}

    async def process_document(self, doc):
        """
        Process a single document
        :param doc:
        :return:
        """
        text = doc.page_content[4000:6000]
        prompt = [{
            "role": "system",
            "content": "You are an expert in extracting job postings from website text content.\n "
        }, {
            "role": "user",
            "content": f"Given the text content of a job posting : {text}\n"
                       f" your task is to extract relevant information related to the posting\n"
                       f"Required information includes the job id, job title, company name\n"
                       f"Optional information includes the job description, job location, job salary, date posted, job type, and url\n"
                       f"If you cannot identify the optional information, you can return 'Unknown' for that field\n"
                       f"There may be multiple job postings in the text content separated by job ids.\n"
                       f"If there are multiple job postings, it is imperative that information does not get mixed up"
                       f"between different postings\n"
                       f"Generally, the number of jobs is determined by the number of job ids found, meaning other fields"
                       f"should not exceed the number of job ids found\n"
        }]
        lc_messages = convert_openai_messages(prompt)

        try:
            llm = ChatOpenAI(model='gpt-4o', temperature=0).with_structured_output(schema=JobListing)
            jobs = await llm.ainvoke(lc_messages)
            return jobs
        except Exception:
            return None
