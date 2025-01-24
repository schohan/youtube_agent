import datetime
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from dotenv import load_dotenv
from app.workflows import ontology_creation_workflow
#from scripts.add_root import add_project_root_to_sys_path
from app.workflows.ontology_creation_workflow import run_workflow

#load env variables from .evn file
load_dotenv()
#add_project_root_to_sys_path()

app = FastAPI()


@app.get("/ping")
async def ping():
    return "pong at " + str(datetime.datetime.now())


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


@app.get("/run_agent")
async def run_agent(topic_category: str):
    print(f"topic_category==>>> {topic_category}")
    resp = await run_workflow(topic_category)
    return {"messages": resp}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
