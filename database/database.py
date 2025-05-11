# Table Scripts
import psycopg2


"""
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth DATE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    topic VARCHAR(255),
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INT REFERENCES conversations(id) ON DELETE CASCADE,
    sender VARCHAR(50), -- 'user' or 'bot'
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


# CONNECT TO DATABASE

def get_db():
    conn = psycopg2.connect(
        dbname="chatbot_db",
        user="postgres",
        password="2802",
        host="localhost",
        port="5432"
    )
    
    conn.autocommit = True
    
    try:
        yield conn
    finally:
        conn.close()
        

def get_chat_history(cur, conversation_id, limit=10):
    cur.execute(""" 
        SELECT * FROM messages 
        WHERE conversation_id = %s
        LIMIT %s
        """, (int(conversation_id), int(limit)))
    chat_history = cur.fetchall()
    return [{"role": "user" if row[2] == "user" else "assistant", "content": row[3]} for row in chat_history]