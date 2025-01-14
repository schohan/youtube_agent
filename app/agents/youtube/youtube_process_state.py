from pydoc_data import topics
from typing import Annotated, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from app.shared.content.youtube_search import VideoStats


class TopicList(BaseModel):
    """
    List of topics that we want to search for on youtube
    """
    topics: List[str] = Field(description="List of topics")


class VideoList(BaseModel):
    """
    List of videos that we want to summarize
    """
    videos: List[VideoStats] = Field(description="List of youtube videos")


class State(TypedDict):
    """
    Intermediate state for the research agent
    """
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]
    done: bool 
    topics: TopicList
    videos: VideoList

    

