import sys 

from pathlib import Path

sys.path.append(str(Path(__file__).parent))

class APIConfig:
    LANGSMITH_API_KEY = 'Your Key'
    GROQ_API_KEY = 'Your Key'
    QDRANT_API_KEY = 'Your Key'
    QDRANT_URL = 'Your URL'
    QDRANT_COLLECTION_NAME = 'Vietnamese_Soliders_chunks'
    TOP_K = 20
    CHAT_HISTORY = 10

class ModelConfig:
    ROOT_DIR = Path(__file__).parent.parent
    # MODEL_NAME = 'llama-3.1-8b-instant'
    MODEL_NAME = 'llama3-70b-8192'
    EMBEDDING_MODEL_NAME = "bkai-foundation-models/vietnamese-bi-encoder"
    TEMPERATURE = 0
    MAX_TOKENS = None
    TIME_OUT = None
    MAX_RETRIES = 2
    