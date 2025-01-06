
from typing import List, Any, Optional
from logging import getLogger

from app.agents.base import BaseAgent
from app.configs.settings import Settings
from app.agents.ontology.researched_state import ResearchedState, MindMapNode, Curriculum
from app.shared.llm.llm_factory import LLMFactory



class OntologyAgent(BaseAgent):
    """
    KeywordResearchAgent is an agent that performs keyword research for a given topic. Keywords are grouped into categories and subcategories.
    
    Attributes:
        settings (Settings): The settings for the agent.
        llm (str): LLM to use for keyword extraction. 
    """
    logger = getLogger(__name__)


    def __init__(self, settings: Settings, tools: list[str]):
        self.settings = settings
        self.model =  settings.openai_model_name 
        self.model_api_key = settings.openai_api_key
        self.editor_model = settings.claude_model_name
        self.editor_api_key = settings.claude_api_key
        self.tools = tools



    async def initialize(self):
        pass


    async def cleanup(self):
        pass

    
    async def _extract_keywords(self, topic: str) -> Any:
        """Extract relevant keywords for a given topic using LLM."""
        
        messages = [
            {"role": "system", "content": f"You are a content editor who understands '{topic}' and how to build curriculum for it. Create a detailed mind map for '{topic}'. Include main branches, sub-branches, and key concepts or ideas for each."}, 
            {"role": "user", "content":  f"topic is: {topic}" }]
        
        print(f"Prompt ==>> {messages}")


        try:
            llm = LLMFactory.get_llm(Settings.llm_openai)
            structured_llm = llm.with_structured_output(schema=Curriculum)

            response = structured_llm.invoke(messages)    
            print(f"response ==>> {response}")

            #raw_content = response.get("choices", [{}])[0].get("message", {}).get("content", None)

            #keywords_list = keywords_str.split(",") if keywords_str != "" else []            
            #researched_keywords = ResearchedKeywords.model_validate_json(raw_content)
            
            
            # researched_keywords = ResearchedKeywords(keywords=raw_content, is_reviewed=False)
            return response
        except Exception as e:
            self.logger.error(f"Error extracting keywords: {str(e)}")
            return None


    # Review content generated for a topic.
    async def review_content(self, topic:str, generated_content: ResearchedState) -> ResearchedState:
        """Review content generated for a topic."""

        messages = [
            {"role": "system", "content": f"Context: You are a content editor who is responsible for creating curriculum for topic {topic}. One of your editors has created the following mind-map of topics to cover in developing curriculum for it. Your task is to review and edit this content to create a final version that can be used to categorize learning topics for this subject."},
            {"role": "user", "content":  "Here is the mindmap created by the editor:\n\n {generated_content}" }              

        ]
        llm = LLMFactory.get_llm(Settings.llm_claude)
        llm.with_structured_output(ResearchedState)

        editor_response =  llm.invoke(messages)   
        
        reviewed_content = editor_response.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        print(f"Reviewed Content ==>> {reviewed_content}")

        return reviewed_content;



    # Execute the agent
    async def execute(self, input: str) -> ResearchedState:
        """
        Given a dictionary of categories and topics, perform keyword research for each topic.
        Use tools to save the keywords as files inside a directory named after the category.        
        Args:
            input (str): The input to the agent containing the topic to research.

        Returns:
            AgentResult: The result of the agent execution            
        """

        try:
            # initialize the agent
            await self.initialize()
            
            # Get keywords for each topic
            curriculum = await self._extract_keywords(input)

            print(f"1 curriculum ==>> {curriculum}") 

            # review content if not already reviewed. Later can be used in a loop
            # if researched_keywords.is_reviewed == False:
            #     reviewed_content = await self._review_content(input, researched_keywords)
            #     researched_keywords.keywords = reviewed_content.keywords
            #     researched_keywords.is_reviewed = True
                

            if curriculum is None:
                self.logger.info(f"No keywords found for topic {input}")
                return ResearchedState(
                    success=False,
                    error=f"No keywords found for topic {input}",
                    curriculum=curriculum,
                    input=input,
                    is_reviewed=False
                )

            return ResearchedState(
                    success=True,
                    error="",
                    curriculum=curriculum,
                    input=input,
                    is_reviewed=Falses
                )

        except Exception as e:
            self.logger.error(f"Research agent error: {str(e)}")
            return ResearchedState(
                success=False,
                error=str(e),
                curriculum=Curriculum(title="", description="", keywords=[]),
                input=input,
                is_reviewed=False
            )
