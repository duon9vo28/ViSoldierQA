import sys 

from pathlib import Path

sys.path.append(str(Path(__file__).parent))

class APIConfig:
    LANGSMITH_API_KEY = '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'
    GROQ_API_KEY = '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'
    QDRANT_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.NuM4zPgiBXg-VHdCkBlVaWVHoS-Dn_6qWU9tQHnF6nM'
    QDRANT_URL = 'https://19cddb00-1635-4336-b06c-6a4605f48e6f.europe-west3-0.gcp.cloud.qdrant.io:6333'
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
    