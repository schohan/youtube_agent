from logging import config
from math import e
import random
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, START, END
from langgraph.graph.message import add_messages
from app.configs.settings import Config
from app.research_agent.utils.state import State, TopicList, VideoList
from langgraph.prebuilt import ToolNode
from app.research_agent.utils.tools import tools
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from typing import Annotated, Literal, TypedDict
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate

from sharedhelpers.storage.file_storage import FileStorage
from sharedhelpers.storage.storage_factory import StorageFactory



tool_node = ToolNode(tools)


research_search_phrases_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a content curator for a website about {category}. You do a great job in finding the most relevant 
             search keywords and key phrases that are commonly used by users on websites and social media sites like youtube.
            """,
        ),
        ("user", "{category}"),
    ]
)

kw_llm = ChatOpenAI(model=Config.openai_model_name, temperature=0) 
# construct the llm with the structured output
topic_llm = research_search_phrases_prompt | kw_llm.with_structured_output(
    schema=TopicList,
)

# Chatbot using OpenAI
yt_search_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a content curator for a website. You do a great job in finding the most relevant 
             content from youtube for a user-provided topic. You look at comment and view counts also to select relevant videos.""",
        ),
        ("user", "{topic}"),
    ]
)
llm = ChatOpenAI(model=Config.openai_model_name, temperature=0) 
llm.bind_tools(tools)


video_llm = yt_search_prompt | llm.with_structured_output(
   schema=VideoList,
)

def find_keywords(state: State):
    """ Find keywords for a given category """
    
    messages = state['messages']

    topicList = topic_llm.invoke({"category":messages[-1].content}, 
                                config={"configurable": {"thread_id": 1}})
    
    print("-->>>  TopicList -> ", topicList)
    #state['topics'] = topicList['topics']
    # We return a list, because this will get added to the existing list
    return  topicList


# Define the function that determines whether to continue or not
def should_continue(state: State) -> str:
    video_list = state["videos"]
    print("Should Continue??? Videos", str(len(video_list.videos)))
   
    # If the LLM makes a tool call, then we route to the "tools" node
    if state["done"] == False:
        return "tools"
    
    # Otherwise, we stop (reply to the user)
    return END



# Define the function that calls the model
def search_youtube(state: State):
    messages = state['messages']

    print("Searching for Topics ", state['topics'])
    #response = llm.invoke(messages)
    topics = state['topics']
    print("Searching vidoes for Topics ", topics) 


    #videoList = video_llm.invoke({"topic": messages[-1].content})
    videoList = {"videos": [{"title": "Video 1", "url": "https://www.youtube.com/watch?v=1"}]}

    print(">>>  VideoList", videoList)

    # state['topics'] = topicList["topics"]

    # decide if tool is needed. If yes, return the name of tool node.
    # if (response["videos"] is not None) and (len(response["videos"]) > 0):
    #     state['done'] = True
    #     state['videos'] = response["videos"]
    #     print("Videos found")
    #     return "tools"
     
    # print("Response", response)

    # We return a list, because this will get added to the existing list
    return videoList






# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
# graph_builder = StateGraph(State)
# #graph_builder.add_node("chatbot", action=chatbot)
# # graph_builder.add_edge(START, "chatbot")
# # graph_builder.add_edge("chatbot", END)


# graph_builder.add_node("node1", action=node1)
# graph_builder.add_edge(START, "node1")
# graph_builder.add_edge("node1", END)
# graph = graph_builder.compile()

