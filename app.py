from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent))


from fastapi import FastAPI, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from middle_ware.cors import setup_cors
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse

from langchain_core.messages import HumanMessage, AIMessage
from sentence_transformers import SentenceTransformer
import asyncio
import psycopg2
from middle_ware.http import LogMiddleWare
from models.LLMChatBot import llmChatbot
import jwt

from PromptTemplate.prompt import PromptTemplate
from config.ModelConfig import APIConfig
from config.DatabaseConfig import getDatabaseConfig
from database import database
from database.database import get_db
from routes.user_service import user_service_router
from routes.registration import registration_router
from schema.model import ChatRequest

# LLM model & Prompts
chatbot = llmChatbot()
chat_chain = chatbot.chat_chain
name_chain = chatbot.name_chain
chat_prompt = PromptTemplate.chat_prompt
name_chatlog_prompt = PromptTemplate.name_chatlog_prompt

# Embedding model
embedding_model = SentenceTransformer('bkai-foundation-models/vietnamese-bi-encoder')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  
SECRET_KEY = "duong28022003"
ALGORITHM = "HS256"


def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    payload = decode_token(token)
    user_id: str = payload.get("sub")
    return int(user_id)

app = FastAPI()
app.add_middleware(LogMiddleWare)
setup_cors(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_service_router)
app.include_router(registration_router)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/scripts", StaticFiles(directory="scripts"), name="scripts")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/chat")
def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/conversations")
def create_conversation(data: ChatRequest, 
                        user_id: int = Depends(get_current_user_id),
                        db=Depends(get_db)):
    cur = db.cursor()
    name_chatlog = name_chain.invoke({"first_rep": data.query})
    topic = name_chatlog.content[:255]

    cur.execute("""
        INSERT INTO conversations (user_id, topic) 
        VALUES (%s, %s) RETURNING id
    """, (user_id, topic))
    conversation_id = cur.fetchone()[0]

    return {"conversation_id": conversation_id}

@app.post("/conversations/{conversation_id}/messages/stream")
async def stream_message(
    conversation_id: int,
    data: ChatRequest,
    db=Depends(get_db)
):
    cur = db.cursor()

    # Lưu câu hỏi của người dùng
    cur.execute("""
        INSERT INTO messages (conversation_id, sender, message) 
        VALUES (%s, 'user', %s)
    """, (conversation_id, data.query))

    # Lấy lịch sử hội thoại
    history_raw = database.get_chat_history(cur, conversation_id, limit=10)
    messages = [
        HumanMessage(content=msg["content"]) if msg["role"] == "user" else AIMessage(content=msg["content"])
        for msg in history_raw
    ]

    # Retrieval
    query_vector = embedding_model.encode(data.query).tolist()
    results = chatbot.qdrant_client.search(
        collection_name=APIConfig.QDRANT_COLLECTION_NAME,
        query_vector=query_vector,
        limit=APIConfig.TOP_K,
    )
    context = "\n\n".join([r.payload["text"] for r in results])

    response_text = ""

    # Stream output
    async def response_generator():
        nonlocal response_text
        async for chunk in chatbot.chat_chain.astream({
            "input": data.query,
            "context": context,
            "messages": messages
        }):
            content = chunk.content
            response_text += content
            yield content
            await asyncio.sleep(0.05)  

        # Lưu phản hồi của bot
        dbname, user, password, host, port = getDatabaseConfig()
        
        with psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            ) as conn:
                with conn.cursor() as cur2:
                    cur2.execute("""
                        INSERT INTO messages (conversation_id, sender, message) 
                        VALUES (%s, 'bot', %s)
                    """, (conversation_id, response_text))
                conn.commit()
    return StreamingResponse(response_generator(), media_type="text/plain")
