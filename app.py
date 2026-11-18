from sqlmodel import Session , select

from database import create_db_and_tables, engine
from models import Users



def main():
    create_db_and_tables()
    # what you want to do here

    


    with Session(engine) as session:


if __name__ == "__main__":
    main()