from langgraph.graph import StateGraph, START, END
from app.agents.ontology.researched_state import ResearchedState
from app.agents.ontology.ontology_agent import OntologyAgent
from app.configs.settings import Settings
import asyncio
from langchain_core.messages import HumanMessage
from typing import Any
import uuid
import os
from app.configs.settings import Settings
from langchain_core.runnables import RunnableConfig
from app.common.content.youtube_search import VideoStats
from app.agents.ontology.topic_ontology import TopicNode, TopicOntology
from app.agents.youtube.youtube_agent import YoutubeAgent
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt
import logging
from typing import Literal
from langgraph.types import Command

from app.common.storage.storage_factory import StorageFactory


# override settings for testing if needed
settings = Settings()
logger = logging.getLogger(__name__)
storage = StorageFactory.get_storage(settings.storage_type, settings.raw_files_dir)


REGENERATE_ONTOLOGY = "regenerate_ontology"
ONTOLOGY_OK = "ontology_ok"

ONTOOGY_NODE_NAME = "youtube_extractor"
YOUTUBE_NODE_NAME = "youtube_extractor"

overwrite_ontology = False
overwrite_youtube = False

# Node for ontology extraction
async def create_ontology_node(state: ResearchedState) -> ResearchedState:    
    logger.info(f"ontology_node: Executing keyword node with inputs==>>>  {state.to_json()}")
    
    
    ontology_file = f"{settings.raw_files_dir}/ontology_{state.input}.json"

    # check if the ontology is already created
    if not overwrite_ontology or storage.has_item(ontology_file):
        logger.info(f"ontology_node: Ontology already created. Loading ontology from file.")
        #state.ontology = TopicOntology.load_ontology(ontology_file, storage)
        loaded_ontology = TopicOntology.load_ontology(storage.get(ontology_file))
        if loaded_ontology is None:
            raise ValueError("Failed to load ontology from storage")
        state.ontology = loaded_ontology
        return state

    agent = OntologyAgent(settings, [])
    res = await agent.execute(state.input)

    logger.info(f"ontology_node: Ontology extraction result==>>> {res}")

    # save the ontology to a json file
    #res.ontology.save_to_json(ontology_file)
    storage.set(ontology_file, res.ontology.to_json_str())
    return res
   

async def ontology_feedback_node(state: ResearchedState) -> str:
    """
    This is a human feedback node for the generated ontology. If the ontology is not satisfactory, the user can provide feedback 
    and the ontology will be regenerated.
    
    Returns:
        str: Either ONTOLOGY_OK or REGENERATE_ONTOLOGY
    """
    logger.info(f"ontology_feedback_node: Executing ontology feedback node with inputs==>>>  {state.to_json()}")
        
    # TODO: fix the conditional edge interruption. 
    feedback = True   #interrupt({"ontology": state.ontology, "question": "Should we regenerate the ontology? (y/n):"})
    logger.info(f"ontology_feedback_node: Feedback==>>> {feedback}")

    # if feedback:
    #     logger.info(f"ontology_feedback_node: Ontology IS approved. Fetch content now.")
    #     return Command(update={"ontology_approved": True, "ontology_review_count": state.ontology_review_count + 1}, goto=YOUTUBE_NODE_NAME) 
    # else:
    #     logger.info(f"ontology_feedback_node: Ontology NOT approved. Regenerate ontology.")
    #     return Command(update={"ontology_approved": False, "ontology_review_count": state.ontology_review_count + 1}, goto=ONTOOGY_NODE_NAME)
    if feedback:
        logger.info(f"ontology_feedback_node: Ontology IS approved. Fetch content now.")
        state.ontology_approved = True
        state.ontology_review_count += 1
        return ONTOLOGY_OK
    else:
        logger.info(f"ontology_feedback_node: Ontology NOT approved. Regenerate ontology.")
        state.ontology_approved = False
        state.ontology_review_count += 1
        return REGENERATE_ONTOLOGY
    


async def youtube_stats_node(state: ResearchedState) -> ResearchedState:
    # state.ontology_approved = True # TODO: move this to Command object in feedback node

    logger.info(f"youtube_node: Executing youtube node with inputs==>>>  {state.to_json()}")
    agent = YoutubeAgent(settings.storage_type)
    
    # Get videos for the keywords based on the ontology
    videos = []
    if overwrite_youtube or not state.videos:
        # download and save videos for the keywords from the ontology
        videos = await agent.download_youtube_videos_for_ontology(state.ontology, state.input)
    else:
        logger.info(f"youtube_node: Videos already downloaded.")
        # load the videos file
        videos = agent.load_videos_from_files(state.input)

    logger.info(f"youtube_node: YouTube extraction result==>>> {videos}")
    state.videos=videos        
    return state



async def test_node(state: ResearchedState) -> ResearchedState:
    """
    This is a test node to test the youtube fetching of limited videos
    """
    logger.info(f"test_node: Executing test node with inputs==>>>  {state.to_json()}")
    topic_ontology = TopicOntology(title="Health", description="test", topics=list())
    
    topic_node = TopicNode(title="Physical Health", children=[])
    topic_node.children.append(TopicNode(title="Cardiovascular", children=[]))
    topic_node.children.append(TopicNode(title="Strength Training", children=[]))
    topic_node.children.append(TopicNode(title="Flexibility", children=[]))
    
    topic_ontology.topics.append(topic_node)

    logger.info(f"test_node: Topic ontology==>>> {topic_ontology}")
    state.ontology = topic_ontology
    return state


async def create_graph():
    """
    This is the main graph for the ontology creation workflow. It is used as a simple workflow. 
    TODO: add conditional nodes to the graph to handle the different workflows
    """
    graph = StateGraph(ResearchedState)
    
    # create the nodes
    graph.add_node('ontology_extractor', create_ontology_node)
    graph.add_node('youtube_extractor', youtube_stats_node)
    graph.add_node('ontology_feedback', ontology_feedback_node)
    
    # create the edges and the graph
    graph.add_edge(START, 'ontology_extractor')
   
   # TODO: conditional edge interruption is not working as expected. Need to fix it.
    graph.add_conditional_edges('ontology_extractor', ontology_feedback_node, path_map={ONTOLOGY_OK: 'youtube_extractor', REGENERATE_ONTOLOGY: 'ontology_extractor'})        
    graph.add_edge('ontology_extractor', 'youtube_extractor')
    graph.add_edge('youtube_extractor', END)
    
    # compile the graph
    memory = MemorySaver()
    app = graph.compile(checkpointer=memory)
    return app



async def create_test_graph():
    """
    This is a test graph for the ontology creation workflow. It is used to test the youtube fetching of limited videos
    """
    graph = StateGraph(ResearchedState)
    graph.add_node('test_node', test_node)
    graph.add_node('youtube_extractor', youtube_stats_node)
    graph.add_edge(START, 'test_node')
    graph.add_edge('test_node', 'youtube_extractor')
    
    graph.add_edge('youtube_extractor', END)

    app = graph.compile()
    return app


async def run_workflow(topic_category: str):
    app = await create_graph()
    thread_config = RunnableConfig(configurable={
            "thread_id": str(uuid.uuid4()),
            "checkpoint_ns": "ontology_workflow",
            "checkpoint_id": str(uuid.uuid4()),
            "interrupt": True
        })
    
    state = ResearchedState(input=topic_category)

    # logger.info(f"main: state==>>> {state.to_json_str()}")
    res = await app.ainvoke(state, config=thread_config)
    return res


async def main():
    input_message = input("\n\nEnter a topic to build a mind map and extract videos for each topic in it: ")  
    res = await run_workflow(input_message)
    logger.info(f"main: state==>>> {res}")
   
if __name__ == "__main__": 
    asyncio.run(main())

   