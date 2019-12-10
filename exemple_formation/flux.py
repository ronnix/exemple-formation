from sqlalchemy import create_engine
from exemple_formation.models import Base


DB_PATH = "exemple.db"


def main():
    engine = create_engine(f"sqlite:///{DB_PATH}") 
    Base.metadata.create_all(engine)

