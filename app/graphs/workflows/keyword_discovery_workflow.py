import stat
from langgraph.graph import StateGraph
from app.agents.keywords.keywords_agent import KeywordResearchAgent, KeywordResearchResult 
from app.configs.settings import Settings
import asyncio
from langchain_core.messages import HumanMessage
from app.graphs.nodes.keyword_node import KeywordNode
from typing import Any
import uuid

settings = Settings()
keyword_agent = KeywordResearchAgent(settings, "gpt-4o", [])    


async def keywords_node(state: dict[str, Any]) -> dict[str, Any]:    
    print(f"Executing keyword node with inputs==>>>  {state}")
      
    #result = await keyword_agent.execute(state)
    node =  KeywordNode(keyword_agent)    
    res = await node.execute(state)
    print(f"result of keyword node==>>> {res}")
    if res['success']:
        state.keywords = res['data']
        state.is_completed = True
    
    return state
   



async def main():
    graph = StateGraph(KeywordResearchResult)
    graph.add_node('keyword', keywords_node)
    graph.set_entry_point('keyword')
    app = graph.compile()

    config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    input_message = input("Enter your topic for keyword extraction: ")

    # for event in graph.stream({"messages": [input_message]}, config, stream_mode="values"):
    #     event["messages"][-1].pretty_print()
    
    state = KeywordResearchResult(user_input=input_message, category="company", keywords=[])
    state_dict = state.model_dump()

    res = await app.ainvoke(state_dict, config)

    print(f"final response ==>>> {res}")
    # for research_result in results.data:   
    #     print(f"\n Topic & Keyword: {research_result}")

if __name__ == "__main__":
    asyncio.run(main())
