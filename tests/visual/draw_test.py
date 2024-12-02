from IPython.display import Image, display
import os
import pytest

import sys
# from app.research_agent.utils.nodes import graph

# Add the root directory of the project to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app.research_agent.utils.nodes import graph

def test_draw():
    """
    Test to draw the graph
    """
    try:
        graph_image = graph.get_graph().draw_mermaid_png()
        with open("graph.png", "wb") as f:
            f.write(graph_image)

        print("Graph saved as graph.png")
    except Exception:
        # This requires some extra dependencies and is optional
        print("Could not draw graph. Please install graphviz and mermaid-cli to draw the graph")


if __name__ == "__main__":
    pytest.main()