
from pydoc_data import topics
from typing import List, Any
from unicodedata import category
import aiohttp
from logging import getLogger
from bs4 import BeautifulSoup
import litellm
from app.agents.base import BaseAgent, AgentResult
from app.configs.settings import Settings
from pydantic import BaseModel
import litellm
from app.shared.content import youtube

class KeywordResearchResult(BaseModel):
    """
    KeywordResearchResult is a model representing the result of keyword research.
    Attributes:
        keywords (List[str]): The keywords that were researched.
    """          
    user_input: str  
    category: str
    keywords: List[str]
    is_completed: bool = False



class KeywordResearchAgent(BaseAgent):
    """
    KeywordResearchAgent is an agent that performs keyword research for a given topic.
    
    Attributes:
        settings (Settings): The settings for the agent.
        llm (str): LLM to use for keyword extraction. 
    """
    logger = getLogger(__name__)


    def track_cost_callback(
        self, 
        kwargs,                 # kwargs to completion
        completion_response,    # response from completion
        start_time, end_time    # start/end time
    ):
        try:
            response_cost = kwargs.get("response_cost", 0)
            print("streaming response_cost", response_cost)
        except:
            pass


    def __init__(self, settings: Settings, model: str, tools: List[str]):
        self.settings = settings
        self.model =  model 
        self.tools = tools
        litellm.success_callback = [self.track_cost_callback]
        # litellm.success_callback = ["lunary", "langfuse", "helicone"]


    async def initialize(self):
        pass


    async def cleanup(self):
        pass

    
    async def _extract_keywords(self, topic: str) -> List[str]:
        """Extract relevant keywords for a given topic using LLM."""
        
        messages = [
            {"role": "system", "content": f"You are a content editor who understands {topic}. Your job is to find the most relevant keywords from the following text. Return list of keywords as comma separated string"}, 
            {"role": "user", "content":  "Extract SEO keywords for this topic: '{topic}'" }]
        
        try:
            # response = litellm.completion(model=self.model,
            #                     messages=messages,
            #                     tools=self.tools,
            #                     tool_choice="auto")  
            response = litellm.completion(model=self.model, messages=messages, temperature=0.0)
            
            keywords_str = response.get("choices", [{}])[0].get("message", {}).get("content", "")

            #print(f"Keywords ==>> {keywords_str}")
            
            return keywords_str.split(",") if keywords_str != "" else []
            # return [keyword.strip() for keyword in keywords_str.split(",") ]
        except Exception as e:
            self.logger.error(f"Error extracting keywords: {str(e)}")
            return []


    async def execute(self, user_input: str) -> AgentResult:
        """
        Given a dictionary of categories and topics, perform keyword research for each topic.
        Use tools to save the keywords as files inside a directory named after the category.        
        Args:
            inputs (Dict[str, Any]): The inputs to the agent are items in the format {category:str, topics: List[str]}

        Returns:
            AgentResult: The result of the agent execution            
        """

        try:
            # initialize the agent
            await self.initialize()
            
            # Get keywords for each topic
            keywords = await self._extract_keywords(user_input)

            print(f"2 Keywords ==>> {keywords}")        
            if keywords is None:
                self.logger.info(f"No keywords found for topic {user_input}")
                return AgentResult(
                    success=False,
                    error=f"No keywords found for topic {user_input}",
                    data=[]
                )

            return AgentResult(
                success=True,
                data=keywords,
                error=""
            )

        except Exception as e:
            self.logger.error(f"Research agent error: {str(e)}")
            return AgentResult(
                success=False,
                error=str(e),
                data=[]
            )
