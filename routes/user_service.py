from fastapi import HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from pathlib import Path
import sys
import jwt
from jwt import PyJWTError as JWTError
from datetime import datetime, timedelta

ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

from psycopg2.extensions import connection
from my_utils.logger import Logger
from database.database import get_db

logger = Logger(log_file='user_auth.log')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Access token

SECRET_KEY = "duong28022003"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: int = 30):
    to_encode = data.copy()
    from datetime import timezone
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def login_user(user_login_field, password, conn: connection):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, username, email, password_hash FROM users
            WHERE username = %s OR email = %s
        """, (user_login_field, user_login_field))
        record = cur.fetchone()
        if not record:
            return JSONResponse(
                status_code=200,
                content={"success": "False", "message": "Không tìm thấy người dùng"}
            )
        
        if record[3] != password:
            logger.log.info(f'User login failed. Entered password: {password}, record password: {record[3]}')
            return JSONResponse(
                status_code=200,
                content={"success": "False", "message": "Mật khẩu không chính xác"}
            )

        access_token = create_access_token(data={"sub": str(record[0])})  # user_id

        logger.log.info(f"User login successfully. User_id: {record[0]}, Access token: {access_token}")

        return JSONResponse(
            status_code=200,
            content={
                "success": 'True',
                "user_id": record[0],
                "access_token": access_token,
                "token_type": "bearer",
                "message": "Đăng nhập thành công"
            }
        )

user_service_router = APIRouter()

@user_service_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), conn=Depends(get_db)):
    # Lấy username và password từ form
    user_login_field = form_data.username
    password = form_data.password
    
    user_login_data = login_user(user_login_field, password, conn)  
    return user_login_data

@user_service_router.get("/conversations")
def get_user_conversations(token: str = Depends(oauth2_scheme), conn=Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError):
        logger.log.info(f"Token {token} expired.")
        raise HTTPException(status_code=401, detail="Phiên đăng nhập đã hết hạn.")
    
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, topic, started_at
            FROM conversations
            WHERE user_id = %s
            ORDER BY started_at DESC
        """, (user_id,))
        conversations = cur.fetchall()
        return [
            {"id": row[0], "topic": row[1], "started_at": row[2].isoformat()}
            for row in conversations
        ]
    
@user_service_router.get("/conversations/{conversation_id}/messages")
def get_messages(conversation_id: int, token: str = Depends(oauth2_scheme), conn=Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError):
        logger.log.info(f"Token {token} expired.")
        raise HTTPException(status_code=401, detail="Phiên đăng nhập đã hết hạn.")
    
    with conn.cursor() as cur:
        # Kiểm tra xem hội thoại có thuộc về người dùng không
        cur.execute("""
            SELECT 1 FROM conversations WHERE id = %s AND user_id = %s
        """, (conversation_id, user_id))
        if not cur.fetchone():
            logger.log.info(f"Unaccessable user. User_id {user_id}. Conversation_id {conversation_id}")
            raise HTTPException(status_code=403, detail="Bạn không có quyền truy cập hội thoại này.")
        
        # Lấy tin nhắn
        cur.execute("""
            SELECT sender, message, timestamp
            FROM messages
            WHERE conversation_id = %s
            ORDER BY timestamp ASC
        """, (conversation_id,))
        
        messages = cur.fetchall()
        return [
            {"sender": row[0], "message": row[1], "timestamp": row[2].isoformat()}
            for row in messages
        ]