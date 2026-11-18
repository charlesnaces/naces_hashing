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
    return {"message": "Sup youre in Users Database"}


@app.get("/users/{id}")
async def read_employee(id):
    with Session(engine) as session:
        print(id,'--------------------------------------------------------------')
        user = session.get(Users, id)
        return {"message": user}
    

@app.post("/users")
async def root(users  : Users):
    with Session(engine) as session:
        session.add(users)
        session.commit()
        session.refresh(users)
        return {"message": users}
    
@app.post("/usersLogin")
async def root(users  : Users):
    with Session(engine) as session:


        print()
        statement = select(Users).where(Users.name == users.name).where(Users.password == users.password)
        results = session.exec(statement)

        # if(results)

        # print('-----------------------------')
        # print(Users.password , users.password)
        # print('-----------------------------')

        result = results.first()
        print(result)

        if (result == None):
            return {"status":"failed"}


        return {
            "status":"success",
            "data": result
            }
    


@app.get("/")
async def root():
    return {"message": "Youre in Specs Database"}


@app.get("/specs/{id}")
async def read_specs(id):
    with Session(engine) as session:
        print(id,'--------------------------------------------------------------')
        spec = session.get(Spec, id)
        return {"message": spec}
    

@app.post("/specs")
async def root(specs  : Specs):
    with Session(engine) as session:
        session.add(specs)
        session.commit()
        session.refresh(specs)
        return {"message": specs}
    
@app.post("/specsLogin")
async def root(specs  : Specs):
    with Session(engine) as session:


        print()
        statement = select(Specs).where(Specs.name == specs.name).where(Specs.password == specs.password)
        results = session.exec(statement)

        # if(results)

        # print('-----------------------------')
        # print(Users.password , users.password)
        # print('-----------------------------')

        result = results.first()
        print(result)

        if (result == None):
            return {"status":"failed"}


        return {
            "status":"success",
            "data": result
            }
    