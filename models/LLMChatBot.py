import sys
from pathlib import Path
import os
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from my_utils.logger import Logger

from qdrant_client import QdrantClient
from config.ModelConfig import ModelConfig, APIConfig
from langchain_groq import ChatGroq

LOGGER = Logger(__file__, log_file='model.log')
LOGGER.log.info('Start Model Serving')
LOGGER.log_model(ModelConfig.MODEL_NAME)

from PromptTemplate.prompt import PromptTemplate

class llmChatbot():
    def __init__(self):
        
        self.set_environment()
        
        self.model = ChatGroq(
            model_name=ModelConfig.MODEL_NAME,
            temperature=ModelConfig.TEMPERATURE,
            max_tokens=ModelConfig.MAX_TOKENS,
            timeout=ModelConfig.TIME_OUT,
            max_retries=ModelConfig.MAX_RETRIES
        )
        
        self.qdrant_client = QdrantClient(
            url = APIConfig.QDRANT_URL,
            api_key= APIConfig.QDRANT_API_KEY
        )
    
        self.chat_chain = PromptTemplate.chat_prompt | self.model
        self.name_chain = PromptTemplate.name_chatlog_prompt | self.model
    
    def set_environment(self):
        os.environ["LANGSMITH_API_KEY"] = APIConfig.LANGSMITH_API_KEY
        os.environ["LANGSMITH_TRACING"] = "true"
        
        os.environ["GROQ_API_KEY"] = APIConfig.GROQ_API_KEY
        os.environ["QDRANT_API_KEY"] = APIConfig.QDRANT_API_KEY