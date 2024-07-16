from langgraph.constants import END
from langgraph.graph import StateGraph

from src.agents.formatter import FormatterAgent
from src.agents.memory.job_state import JobAgentState
from src.agents.review import ReviewAgent
from src.agents.scraper import ScraperAgent
from src.agents.search import SearchAgent
from src.agents.semantics import SemanticsAgent


class MasterAgent:
    def __init__(
            self,
            query: str,
            sources=None,
            max_results: int = 5
    ):
        if sources is None:
            sources = ['https://www.linkedin.com/']
        self.query = query
        self.sources = sources
        self.max_results = max_results

    def init_graph(self):
        """
        Initialize the state graph with all nodes and edges
        :return: StateGraph(JobAgentState)
        """
        semantics_agent = SemanticsAgent()
        search_agent = SearchAgent(providers=self.sources)
        scraper_agent = ScraperAgent()
        formatter_agent = FormatterAgent()
        review_agent = ReviewAgent()

        builder = StateGraph(JobAgentState)

        builder.add_node('semantics', semantics_agent.clarify_query)
        builder.add_node('search', search_agent.find_job_urls)
        builder.add_node('scraper', scraper_agent.scrape_html)
        builder.add_node('formatter', formatter_agent.format)
        builder.add_node('review', review_agent.review)
        builder.add_node('revise', review_agent.revise_query)

        builder.add_conditional_edges(
            'semantics',
            semantics_agent.passes_semantics,
            {False: END, True: 'search'}
        )
        builder.add_edge('search', 'scraper')

        builder.add_edge('scraper', 'formatter')
        builder.add_conditional_edges(
            'formatter',
            review_agent.revise,
            {False: 'review', True: 'revise', 'END': END}
        )
        builder.add_edge('revise', 'search')

        builder.set_entry_point('semantics')
        builder.set_finish_point('review')

        return builder

    async def run(self):
        """
        Run the agents in the state graph given the initial state query, field, and companies
        :return: List[Job]
        """
        graph = self.init_graph()
        chain = graph.compile()

        result = await chain.ainvoke(
            {
                'initial_query': self.query,
                'max_results': self.max_results,
                'sources': self.sources,
                'max_revisions': 2,
            }
        )

        return result
