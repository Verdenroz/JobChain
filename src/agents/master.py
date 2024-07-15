import time

from langgraph.constants import END
from langgraph.graph import StateGraph

from src.agents.job_state import JobAgentState
from src.agents.scraper import ScraperAgent
from src.agents.search import SearchAgent
from src.agents.semantics import SemanticsAgent


class MasterAgent:
    def __init__(self, query: str):
        self.task_id = int(time.time())
        self.query = query

    @staticmethod
    def init_graph():
        semantics_agent = SemanticsAgent()
        search_agent = SearchAgent()
        scraper_agent = ScraperAgent()

        builder = StateGraph(JobAgentState)

        builder.add_node('semantics', semantics_agent.clarify_query)
        builder.add_node('search', search_agent.find_job_urls)
        builder.add_node('scraper', scraper_agent.scrape_html)

        builder.add_conditional_edges('semantics',
                                      semantics_agent.passes_semantics,
                                      {False: END, True: 'search'}
                                      )
        builder.add_edge('search', 'scraper')

        builder.set_entry_point('semantics')
        builder.set_finish_point('scraper')

        return builder

    async def run(self):
        graph = self.init_graph()
        chain = graph.compile()

        result = await chain.ainvoke({'initial_query': self.query})

        return result
