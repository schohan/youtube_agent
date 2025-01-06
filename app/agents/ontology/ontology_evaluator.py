from app.agents.ontology.researched_state import ResearchedState
from app.agents.ontology.ontology_agent import OntologyAgent
from typing import Any

class OntologyEvaluatorNode:
    def __init__(self, agent: OntologyAgent):
        self.agent = agent

    async def execute(self, agent_state: ResearchedState) -> ResearchedState:
        print(f"Evaluating generated keywords ----> {agent_state.input}")
        agent_result = await self.agent.execute(agent_state)

        print(f"In keyword node with agent_result ----> {agent_result}")    

        return agent_result.model_dump()
    
    