from app.agents.keywords.keywords_agent import KeywordResearchAgent
from typing import Any

class KeywordNode:
    def __init__(self, agent: KeywordResearchAgent):
        self.agent = agent

    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        print(f"Executing keyword node with inputs ----> {state.user_input}")
        agent_result = await self.agent.execute(state.user_input)

        print(f"In keyword node with agent_result ----> {agent_result}")    

        return agent_result.model_dump()
    
    