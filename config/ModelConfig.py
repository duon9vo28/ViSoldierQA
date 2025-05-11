import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

# from dotenv import load_dotenv
# load_dotenv()  

class APIConfig:
    LANGSMITH_API_KEY = os.getenv('LANGSMITH_API_KEY', '')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    QDRANT_API_KEY = os.getenv('QDRANT_API_KEY', '')
    QDRANT_URL = os.getenv('QDRANT_URL', '')
    QDRANT_COLLECTION_NAME = os.getenv('QDRANT_COLLECTION_NAME', 'Vietnamese_Soliders_chunks')
    TOP_K = int(os.getenv('TOP_K', 20))
    CHAT_HISTORY = int(os.getenv('CHAT_HISTORY', 10))

class ModelConfig:
    ROOT_DIR = Path(__file__).parent.parent
    MODEL_NAME = os.getenv('MODEL_NAME', 'llama3-70b-8192')
    EMBEDDING_MODEL_NAME = os.getenv('EMBEDDING_MODEL_NAME', 'bkai-foundation-models/vietnamese-bi-encoder')
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0))
    MAX_TOKENS = os.getenv('MAX_TOKENS')
    TIME_OUT = os.getenv('TIME_OUT')
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 2))
