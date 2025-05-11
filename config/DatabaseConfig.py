import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

# from dotenv import load_dotenv
# load_dotenv()  

class DatabaseConfig:
    POSTGRES_USER=os.getenv('POSTGRES_USER','')
    POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD','')
    POSTGRES_DB=os.getenv('POSTGRES_DB','')
    HOST="localhost"
    PORT="5432"

def getDatabaseConfig():
    return (DatabaseConfig.POSTGRES_USER, 
            DatabaseConfig.POSTGRES_PASSWORD, 
            DatabaseConfig.POSTGRES_DB, 
            DatabaseConfig.HOST, 
            DatabaseConfig.PORT)

print(DatabaseConfig.POSTGRES_USER)