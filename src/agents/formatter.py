import requests

from src.schemas.job import Job
from src.agents.memory.job_state import JobAgentState


class FormatterAgent:
    def __init__(self):
        pass

    async def is_valid_url(self, url):
        """
        Check if a URL is valid
        :param url:
        :return:
        """
        try:
            response = requests.get(url)
            return response.status_code == 200
        except Exception:
            return False

    async def format(self, state: JobAgentState):
        """
        Format the job listings into a List[Job]
        :param state:
        :return:
        """
        job_listings = state['job_listings']
        max_results = state['max_results']
        formatted_jobs = []

        for listing in job_listings:
            num_jobs = len(listing.job_id)

            for i in range(num_jobs):

                if len(formatted_jobs) >= max_results:
                    break

                job = Job(
                    job_title=listing.job_title[i] if i < len(listing.job_title) else None,
                    job_company=listing.job_company[i] if i < len(listing.job_company) else None,
                    job_description=listing.job_description[i] if listing.job_description and i < len(
                        listing.job_description) else None,
                    job_location=listing.job_location[i] if listing.job_location and i < len(
                        listing.job_location) else None,
                    job_posted_date=listing.job_posted_date[i] if listing.job_posted_date and i < len(
                        listing.job_posted_date) else None,
                    job_type=listing.job_type[i] if listing.job_type and i < len(listing.job_type) else None,
                    job_salary=listing.job_salary[i] if listing.job_salary and i < len(
                        listing.job_salary) else None,
                    url=listing.urls[i] if listing.urls and i < len(listing.urls) and await self.is_valid_url(
                        listing.urls[i]) else None,
                )

                formatted_jobs.append(job)

        return {"jobs": formatted_jobs}
