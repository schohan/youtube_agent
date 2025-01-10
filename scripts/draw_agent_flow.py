from IPython.display import Image, display
import asyncio
from app.workflows.ontology_creation_workflow import create_graph



async def draw_agent_flow(file_path: str = "docs/agent_flow_graph.png"):
    """
    Draw the agentic flow graph and save it to a file

    Args:
        file_path (str): The file path to save the graph to

    Returns:
        None
    """
    try:
        app = await create_graph()
        graph_image = app.get_graph().draw_mermaid_png()
        with open(file_path, "wb") as f:
            f.write(graph_image)

        print("Graph saved as graph.png")
    except Exception:
        # This requires some extra dependencies and is optional
        print("Could not draw graph. Please install graphviz and mermaid-cli to draw the graph")


async def main():
    await draw_agent_flow()

if __name__ == "__main__":
    asyncio.run(main())
