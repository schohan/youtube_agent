from app.configs.settings import Settings


class LLMFactory:
    """
    Factory class to get LLM instance based on model name
    """

    @staticmethod
    def get_llm(llm: str):
        """
        Factory method to get LLM instance based on model name

        Args:
            model_name (str): The model name to use. e.g. openai
        Returns:
            Langchain llm object (see BaseChatModel for details): An subclass of BaseChatModel 
        """
        if llm == Settings.llm_openai:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(model=Settings.openai_model_name, temperature=Settings.openai_model_temperature) 
        else:
            raise ValueError("Invalid model name")         
