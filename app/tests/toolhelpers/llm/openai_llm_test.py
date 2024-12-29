from app.configs.settings import Config
from app.configs.logging_config import get_logger

logger = get_logger(__name__)


def test_invoke():
    logger.info("Running test_invoke")
    # llm = LLMFactory.get_llm("openai")
