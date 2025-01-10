from typing import final
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END

from app.research_agent.utils.nodes import tool_node, should_continue, search_youtube, find_keywords
from app.research_agent.utils.state import State


workflow = StateGraph(State)

# Define the two nodes we will cycle between
#workflow.add_node("find_keywords", find_keywords)
workflow.add_node("youtube_agent", search_youtube)
#workflow.add_node("tools", tool_node)

# Set the entrypoint as `agent`
# This means that this node is the first one called
workflow.add_edge(START, "youtube_agent")
# workflow.add_edge("find_keywords", "search_youtube")

# We now add a conditional edge
# workflow.add_conditional_edges(
#     # First, we define the start node. We use `agent`.
#     # This means these are the edges taken after the `agent` node is called.
#     "youtube_agent",
#     # Next, we pass in the function that will determine which node is called next.
#     should_continue,
# )

# We now add a normal edge from `tools` to `youtube_agent`.
# This means that after `tools` is called, `youtube_agent` node is called next.
#workflow.add_edge("tools", 'youtube_agent')
workflow.add_edge("youtube_agent", END)
# Initialize memory to persist state between graph runs
checkpointer = MemorySaver()

# Finally, we compile it!
# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable.
# Note that we're (optionally) passing the memory when compiling the graph
app = workflow.compile(checkpointer=checkpointer)



def start_agent(user_input: str | list[str], thread_id: int ):

    final_state = app.invoke(
        {"topics": user_input},
        config={"configurable": {"thread_id": thread_id}}
    )   
    print("=>>> End of agent run <==", final_state)

    return final_state





# def download_youtube_videos(query: str):
#     """
#     Get youtube videos based on a query

#     Args:
#         query (str): The query to search for

#     Returns:
#         results (list): A list of dictionaries with video details
#     """

#     api_key = Config.youtube_api_key # os.environ.get("YOUTUBE_API_KEY")
#     max_results = Config.max_youtube_results # int(os.environ.get("MAX_YOUTUBE_RESULTS", 10))

#     print("Config.youtube_api_key " + api_key)

#     results = search_youtube_videos(query, api_key)
#     return results


# def process_raw_videos():
#     """
#     Process raw downloaded youtube videos from configured raw video location. Processing involves:
#      a. Summarizing videos using transcript
#      b. Save processed objects along with metadata to storage for use by application

#     Args:
#         None

#     Returns:
#         None
#     """
#     # 
#     # process all files in the given directory. Use supplied functions to process the files
#     # TODO: Implement this function  
#     return f"{__name__} Not implemented"
    


# def stream_graph_updates(user_input: str):
#     for event in graph.stream({"messages": [("user", user_input)]}):
#         for value in event.values():
#             print("Assistant:", value["messages"][-1].content)
#             return value["messages"][-1].content

# graph.stream({"messages": [("user", "asthma treatments")]})

#download_youtube_videos("asthma treatments")

