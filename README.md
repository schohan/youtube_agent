# Youtube Agent (WORK IN PROGRESS)
> NOTE: This code is actively being worked on and is not finished for use yet.

## Overview

Youtube agent finds videos for given topics using Youtube API. 
For each video in the result set, it generates content summary and store it along with the metadata for consumption by an API or application.

Extracted metadata includes video title, published date, view count, comment counts, transcript, captions, and more.

## Purpose 

This agent is a TL;DR for the Youtube videos. It generates summaries of the youtube videos to be consumed by applications.

There can be thousands of Youtube videos for a given topic and even though Youtube has its own algorithm to bubble up the best ones to the top, it is still difficult to watch all of the videos unless one has hours of time to spare.  

Applications built on top of this agent can help pinpoint the videos relevant to your needs. 


## Installation

Install poetry with pipx

```bash
pipx install poetry
```

See [Installation Steps](https://python-poetry.org/docs/#installing-with-pipx)

## Adding packages

```bash
# create and activate a vitual env.
python -m venv venv
source venv/bin/activate (or use <venv>\Scripts\activate.bat for windows)

# in virtual environment, add packages from pyproject.toml
poetry install
```

## Setup LangSmith (Optional)
LangSmith will help us trace, monitor and debug LangChain applications. 
You can sign up for LangSmith [here](https://smith.langchain.com/). 
If you don't have access, you can skip this section


```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # if not specified, defaults to "default"
```

## Launch LangServe

```bash
langchain serve
```

## Running in Docker

This project folder includes a Dockerfile that allows you to easily build and host your LangServe app.

### Building the Image

To build the image, you simply:

```shell
docker build . -t youtube-agent-app
```

If you tag your image with something other than `youtube-agent-app`,
note it for use in the next step.

### Running the Image Locally

To run the image, you'll need to include any environment variables
necessary for your application.

In the below example, we inject the `OPENAI_API_KEY` environment
variable with the value set in my local environment
(`$OPENAI_API_KEY`)

We also expose port 8080 with the `-p 8080:8080` option.

```shell
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -p 8080:8080 youtube-agent-app
```

### Run tests

