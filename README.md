
# JobChain

JobChain currently has one semi-functioning task: aggregating jobs from LinkedIn using `Langgraph` and `Tavily`. It can be run locally through either FastAPI or by calling the agents directly. See `Getting Started` below for more details.

 It is very much still **WIP**, but it can serve as an introductory tutorial into the basics of multi-agent frameworks.

## Architechture

<p align="center">
  <img src="https://github.com/Verdenroz/JobChain/blob/master/assets/graph.png?raw=true" alt="JobChain Graph"/>
</p>

There are six nodes:

    1   Semantics   ->  ensures queries are relevant and concise
    2   Search      ->  searches for urls to scrape with Tavily
    3   Scraper     ->  scrapes job listings
    4   Formatter   ->  formats job listings into lists of readable jobs
    5   Review      ->  reviews formatted jobs for missing information
    6   Revise      ->  revises query if no jobs have been found

#### Conditional Edges

There are two conditional edges:

    1.  Semantics   ->      Search if initial query is relevant to jobs | End if initial query is irrelevant to jobs
    2.  Formatter   ->      Revise if no jobs were found |  Review if jobs were found | End if revision count is > max revisions
    
## Roadmap

- Additional support for different job boards

- Resume writing/editing

- Cover leter generation


## API Reference

#### Find jobs by query

```
  GET /jobs
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `query` | `string` | **Required**. Your query |
| `source` | `string` | **Optional**. Your job board (`https://www.linkedin.com/`) |
| `max_results` | `int` | **Optional**.  The maximum number of jobs to return ***(Default: 5)***|

## Sample Output
```json
  [
  {
    "job_title": "2025 Software Engineer Program - Summer Internship (Code for Good Hackathon) - United States",
    "job_company": "JPMorganChase",
    "job_description": "Unknown",
    "job_location": "Atlanta, GA",
    "job_posted_date": "1 week ago",
    "job_type": "Unknown",
    "job_salary": "Unknown",
    "url": "https://www.linkedin.com/jobs/view/2025-software-engineer-program-summer-internship-code-for-good-hackathon-united-states-at-jpmorganchase-3966841880?position=3&pageNum=0&refId=TtqafpgcvsMyNH0jPDPg3A%3D%3D&trackingId=wrtSvecn7wOiWWOpZ0P5gA%3D%3D&trk=public_jobs_jserp-result_search-card"
  },
  {
    "job_title": "Fall 2024 Undergraduate Software Engineering Co-Op/Intern",
    "job_company": "AMD",
    "job_description": "Unknown",
    "job_location": "Austin, TX",
    "job_posted_date": "2 days ago",
    "job_type": "Unknown",
    "job_salary": "Unknown",
    "url": "https://www.linkedin.com/jobs/view/fall-2024-undergraduate-software-engineering-co-op-intern-at-amd-3905505743?position=4&pageNum=0&refId=TtqafpgcvsMyNH0jPDPg3A%3D%3D&trackingId=V7JI77xKCaBwVR9HsZjXww%3D%3D&trk=public_jobs_jserp-result_search-card"
  },
  {
    "job_title": "Project Management, Software Engineering Student Fall 2024",
    "job_company": "EV.Careers",
    "job_description": null,
    "job_location": "Troy, MI",
    "job_posted_date": "4 days ago",
    "job_type": null,
    "job_salary": null,
    "url": "https://edin.com/jobs/view/project-management-software-engineering-student-fall-2024-at-ev-careers-3971165680?position=2&pageNum=0&refId=%2BYiWgvpj%2BX2hYG28a%2F0afw%3D%3D&trackingId=zZwIBrrb29fwuWLM5%2FTLaQ%3D%3D&trk=public_jobs_jserp-result_search-card"
  },
  {
    "job_title": "Systems Engineer Co-op - Spring 2025",
    "job_company": "RoviSys Building Technologies",
    "job_description": null,
    "job_location": "Peachtree City, GA",
    "job_posted_date": "5 days ago",
    "job_type": null,
    "job_salary": null,
    "url": "https://www.linkedin.com/jobs/view/systems-engineer-co-op-spring-2025-at-rovisys-building-technologies-3973027879?position=3&pageNum=0&refId=%2BYiWgvpj%2BX2hYG28a%2F0afw%3D%3D&trackingId=GyQy4xgBuVjxVKDjN72lQQ%3D%3D&trk=public_jobs_jserp-result_search-card"
  },
  {
    "job_title": "Fall 2024 Application Engineering Intern",
    "job_company": "Ansys",
    "job_description": null,
    "job_location": "Austin, TX",
    "job_posted_date": "Unknown",
    "job_type": null,
    "job_salary": null,
    "url": "https://www.linkedin.com/jobs/view/fall-2024-application-engineering-intern-at-ansys-3977404174?position=4&pageNum=0&refId=%2BYiWgvpj%2BX2hYG28a%2F0afw%3D%3D&trackingId=PvPpfTk2FojDpaRP%2BdMfHg%3D%3D&trk=public_jobs_jserp-result_search-card"
  }
]
```


## Cost

Cost and time needed depends on `max_results` and if jobs were scraped with enough information. The agents use a combination of gpt-3.5-turbo and gpt-4o, but most of the tokens belong to the scraping, which uses gpt-4o. On average, requests take about ~15s assuming `max_results=5`.

Assuming the worst case scenario with `max_results=5` and all five jobs needed to be reviewed:

*Total tokens ~= 25000 and 30 seconds*

**Costs** ~$0.0125 Worst case


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`TAVILY_API_KEY`

`OPENAI_API_KEY`


## Getting Started

Clone the project

```bash
  git clone https://github.com/Verdenroz/JobChain.git
```
Go to the project directory

```bash
  cd JobChain
```
Install dependencies

```bash
  pip install -r requirements.txt
```
Start the server with FastAPI

```bash
  python -m uvicorn main:app --reload
```

## Known Issues

  -  BeautifulSoup Transformer and HTML2Text both struggle to scrape salary, job description, and job type. Manual scraping may be a solution
  -  Multiple sources query params are unreliable due to Tavily API's `include_domains` arg in searching. Including two-three domains seems to return zero urls.

## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.

