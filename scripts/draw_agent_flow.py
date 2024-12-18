from IPython.display import Image, display
import os
import sys
# from app.research_agent.utils.nodes import graph

# Add the root directory of the project to sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from app.research_agent.agent import app



def draw_agent_flow(file_path: str = "docs/agent_flow_graph.png"):
    """
    Draw the agentic flow graph and save it to a file

    Args:
        file_path (str): The file path to save the graph to

    Returns:
        None
    """
    try:
        graph_image = app.get_graph().draw_mermaid_png()
        with open(file_path, "wb") as f:
            f.write(graph_image)

        print("Graph saved as graph.png")
    except Exception:
        # This requires some extra dependencies and is optional
        print("Could not draw graph. Please install graphviz and mermaid-cli to draw the graph")


def main():
    draw_agent_flow()

if __name__ == "__main__":
    main()