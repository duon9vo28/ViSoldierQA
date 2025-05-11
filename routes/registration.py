from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent))


from fastapi import  Depends, Request, Query, Form,  APIRouter
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from pydantic import EmailStr
import psycopg2

from schema.model import RegisterForm
from datetime import datetime
from my_utils.logger import Logger
from database.database import get_db

logger = Logger(log_file='user_auth.log')

registration_router = APIRouter()

templates = Jinja2Templates(directory="templates")

@registration_router.get("/registration")
def registration_page(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})

@registration_router.get("/registration/authorization")
def check_availability(
    username: str = Query(...),
    email: str = Query(...),
    db=Depends(get_db)
):
    with db.cursor() as cur:
        cur.execute("SELECT 1 FROM users WHERE username = %s", (username,))
        if cur.fetchone():
            return JSONResponse(content={"available": False, "message": "Tên đăng nhập đã được sử dụng."})

        cur.execute("SELECT 1 FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            return JSONResponse(content={"available": False, "message": "Email đã được sử dụng."})

    return JSONResponse(content={"available": True})


def as_form(
    name: str = Form(...),
    dob: str = Form(...),
    username: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...)
) -> RegisterForm:
    return RegisterForm(name=name, dob=dob, username=username, email=email, password=password)


@registration_router.post("/register")
async def register_user(
    form_data: RegisterForm = Depends(as_form),
    db=Depends(get_db)
):

    with db.cursor() as cur:
        cur.execute("SELECT 1 FROM users WHERE username = %s", (form_data.username,))
        if cur.fetchone():
            logger.log.info(f"Existed username: {form_data.username}")
            return JSONResponse(status_code=400, content={"message": "Tên đăng nhập đã tồn tại."})

        cur.execute("SELECT 1 FROM users WHERE email = %s", (form_data.email,))
        if cur.fetchone():
            logger.log.info(f"Existed email: {form_data.email}")
            return JSONResponse(status_code=400, content={"message": "Email đã tồn tại."})

        dob_obj = datetime.strptime(form_data.dob, "%d/%m/%Y") 
        dob_sql = dob_obj.strftime("%Y-%m-%d")

        cur.execute("""
            INSERT INTO users (name, date_of_birth, username, email, password_hash)
            VALUES (%s, %s, %s, %s, %s)
        """, (form_data.name, dob_sql, form_data.username, form_data.email, form_data.password))

    logger.log.info(f"Username {form_data.username} registration accepted.")
    return JSONResponse(status_code=200, content={"message": "Đăng ký thành công!"})
