import random
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from app.configs.app_config import Config
from app.research_agent.utils.state import State
from app.research_agent.utils.tools import search_youtube_videos, summarizer, find_search_terms_for_topic 

# Chatbot using OpenAI
llm = ChatOpenAI(model=Config.model_name, temperature=0) 
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


# Test nodes to test the graph
def node1(state: State):
    topic = random.choice(["asthma", "covid"])

    return {"messages": find_search_terms_for_topic(topic) }


# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder = StateGraph(State)
#graph_builder.add_node("chatbot", action=chatbot)
# graph_builder.add_edge(START, "chatbot")
# graph_builder.add_edge("chatbot", END)


graph_builder.add_node("node1", action=node1)
graph_builder.add_edge(START, "node1")
graph_builder.add_edge("node1", END)
graph = graph_builder.compile()

