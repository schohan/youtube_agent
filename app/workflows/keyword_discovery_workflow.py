import stat
from langgraph.graph import StateGraph, START, END

from app.agents.ontology.researched_state import ResearchedState
from app.agents.ontology.ontology_agent import OntologyAgent
from app.configs.settings import Settings
import asyncio
from langchain_core.messages import HumanMessage
#from app.agents.keywords.keyword_node import KeywordNode
from typing import Any
import uuid
import os
from app.configs.settings import Settings


settings = Settings()


# Node for ontology extraction
async def ontology_node(state: ResearchedState) -> ResearchedState:    
    print(f"ontology_node: Executing keyword node with inputs==>>>  {state.to_json()}")
      
    agent = OntologyAgent(settings, [])
    res = await agent.execute(state.input)
    # res = state
    print(f"ontology_node: Ontology extraction result==>>> {res}")
    return res
   

async def main():
    graph = StateGraph(ResearchedState)
    graph.add_node('ontology_extractor', ontology_node)
    graph.add_edge(START, 'ontology_extractor')
    graph.add_edge('ontology_extractor', END)

    app = graph.compile()


    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    input_message =  "health" # input("Enter your topic for keyword extraction: ")  

    state = ResearchedState(input=input_message)

    # for event in graph.stream({"messages": [input_message]}, config, stream_mode="values"):
    #     event["messages"][-1].pretty_print()
    print(f"main: state==>>> {state.to_json_str()}")
    res = await app.ainvoke(state, config=config)

    print("final response ==>>> {}".format(res))
    # for research_result in results.data:   
    #     print(f"\n Topic & Keyword: {research_result}")

if __name__ == "__main__":
    asyncio.run(main())
   