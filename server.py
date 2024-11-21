from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from app.research_agent.agent import stream_graph_updates
from dotenv import load_dotenv

#load env variables from .evn file
load_dotenv()

app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


@app.get("/chat")
async def chat(q: str):
    resp = stream_graph_updates(q)
    return {"messages": resp}

# Edit this to add the chain you want to add
#add_routes(app, NotImplemented)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
