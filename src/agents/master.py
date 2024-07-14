import time

from langgraph.constants import END
from langgraph.graph import StateGraph

from schemas.job import JobAgentState
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

        builder = StateGraph(JobAgentState)

        builder.add_node('semantics', semantics_agent.clarify_query)
        builder.add_node('search', search_agent.find_jobs)

        builder.add_conditional_edges('semantics',
                                      semantics_agent.get_semantics,
                                      {END: END, 'search': 'search'}
                                      )

        builder.set_entry_point('semantics')
        builder.set_finish_point('search')

        return builder

    async def run(self):
        graph = self.init_graph()
        chain = graph.compile()

        result = await chain.ainvoke({'query': self.query})

        return result
