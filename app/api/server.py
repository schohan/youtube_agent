import datetime
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from app.research_agent.agent import stream_graph_updates, download_youtube_videos
from dotenv import load_dotenv
from scripts.add_root import add_project_root_to_sys_path

#load env variables from .evn file
load_dotenv()
add_project_root_to_sys_path()

app = FastAPI()


@app.get("/ping")
async def ping():
    return "pong at " + str(datetime.datetime.now())


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


@app.get("/download_youtube_videos")
async def check(q: str):
    resp = download_youtube_videos(q)
    return {"messages": resp}

@app.get("/chat")
async def chat(q: str):
    resp = stream_graph_updates(q)
    return {"messages": resp}

# Edit this to add the chain you want to add
#add_routes(app, NotImplemented)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
