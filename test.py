import hashlib
from re import fullmatch

from fastapi import FastAPI
from sqlmodel import Session , select
from contextlib import asynccontextmanager
from database import create_db_and_tables, engine
from fastapi.middleware.cors import CORSMiddleware

from models import Users
from models import Specs

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


origins = [
    "http://localhost:3000",  # React development server
    "https://example.com",    # Production frontend
    "*"
] # Define allowed origins (domains that can access your API)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Allow these origins
    allow_credentials=True,       # Allow cookies, authentication headers
    allow_methods=["*"],          # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],          # Allow all headers
)



@app.get("/")
async def root():
    return {"Meow"}


@app.get("/users/{id}")
async def read_employee(id):
    with Session(engine) as session:
        print(id,'--------------------------------------------------------------')
        user = session.get(Users, id)
        if user is None:
            return {"message": None}
        message = {"id": user.id, "username": user.username}
        if fullmatch(r"[0-9a-f]{64}", user.password):
            message["password"] = user.password
        return {"message": message}
    

@app.post("/users")
def create_user(users: Users):
    users.password = hashlib.sha256(users.password.encode()).hexdigest()
    with Session(engine) as session:
        session.add(users)
        session.commit()
        session.refresh(users)
        return {"message": users}
    
@app.post("/usersLogin")
def login(users: Users):
    input_hashed = hashlib.sha256(users.password.encode()).hexdigest()
    with Session(engine) as session:
        statement = select(Users).where(Users.username == users.username)
        for user in session.exec(statement):
            if user.password == input_hashed:
                return {"status": "success"}
            if user.password == users.password and not fullmatch(r"[0-9a-f]{64}", user.password):
                user.password = input_hashed
                session.commit()
                return {"status": "success"}

    return {"status": "failed"}
    



@app.get("/specs/{id}")
async def read_specs(id: int):
    with Session(engine) as session:
        spec = session.get(Specs, id)
        return {"message": spec}


@app.post("/specs")
async def save_specs(specs: Specs):
    with Session(engine) as session:
        session.add(specs)
        session.commit()
        session.refresh(specs)
        return {"message": specs}
