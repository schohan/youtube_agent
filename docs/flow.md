# Flow of Research Agent

Youtube Research Agent does the following given an instruction to research on a topic:

- Searches for videos on youtbube using Youtube tool for a given topic query
- Based on the instructions, it filter out the videos that don't meet the criteria
- Present videos and meta data along with a paragraph describing it in a markdown or json format

## Flow
```mermaid
graph TD
    A[Start] --> B[Receive instruction to research on a topic]
    B --> C[Search for videos on YouTube using YouTube tool for the given topic query]
    C --> D[Filter out videos that don't meet the criteria based on the instructions]
    D --> E[Present videos and metadata along with a paragraph describing it in markdown or JSON format]
    E --> F[End]
```
