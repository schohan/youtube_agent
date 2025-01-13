import stat
from turtle import title
from langgraph.graph import StateGraph, START, END

from app.agents.ontology import topic_ontology
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
from langchain_core.runnables import RunnableConfig
from app.shared.content.youtube_search import YouTubeSearcher
from app.shared.content.youtube_search import VideoStats
from app.agents.ontology.topic_ontology import TopicNode, TopicOntology
settings = Settings()

# Node for ontology extraction
async def ontology_node(state: ResearchedState) -> ResearchedState:    
    print(f"ontology_node: Executing keyword node with inputs==>>>  {state.to_json()}")
      
    agent = OntologyAgent(settings, [])
    res = await agent.execute(state.input)
    # res = state
    print(f"ontology_node: Ontology extraction result==>>> {res}")
    return res
   

async def youtube_node(state: ResearchedState) -> ResearchedState:
    print(f"youtube_node: Executing youtube node with inputs==>>>  {state.to_json()}")
    agent = YouTubeSearcher(settings.youtube_api_key)
    
    # TODO get videos for the keywords based on the ontology
    
    videos = []
    #videos: list[VideoStats] = await agent.search_videos(state.input)

    # get keywords from the ontology
    await agent.download_youtube_videos_for_ontology(state.ontology, 30)
    #keywords = state.ontology.get_keywords()
    #print(f"youtube_node: Keywords==>>> {keywords}")

    # TODO attach tool to save videos to storage

    print(f"youtube_node: YouTube extraction result==>>> {videos}")
    state.videos=videos        
    return state


async def test_node(state: ResearchedState) -> ResearchedState:
    """
    This is a test node to test the youtube fetching of limited videos
    """
    print(f"test_node: Executing test node with inputs==>>>  {state.to_json()}")
    topic_ontology = TopicOntology(title="Health", description="test", topics=list())
    
    topic_node = TopicNode(title="Physical Health", children=[])
    topic_node.children.append(TopicNode(title="Cardiovascular", children=[]))
    topic_node.children.append(TopicNode(title="Strength Training", children=[]))
    topic_node.children.append(TopicNode(title="Flexibility", children=[]))
    
    topic_ontology.topics.append(topic_node)

    print(f"test_node: Topic ontology==>>> {topic_ontology}")
    state.ontology = topic_ontology
    return state


async def create_graph():
    graph = StateGraph(ResearchedState)
   # graph.add_node('ontology_extractor', ontology_node)
    graph.add_node('youtube_extractor', youtube_node)
    graph.add_node('test_node', test_node)
   # graph.add_edge(START, 'ontology_extractor')
   # graph.add_edge('ontology_extractor', 'youtube_extractor')
    graph.add_edge(START, 'test_node')
    graph.add_edge('test_node', 'youtube_extractor')
    
    graph.add_edge('youtube_extractor', END)

    app = graph.compile()
    return app


async def main():
    app = await create_graph()
    config = RunnableConfig(metadata={"thread_id": str(uuid.uuid4())})
    input_message =  input("Enter your topic for keyword extraction: ")  

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
   