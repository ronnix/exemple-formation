from argparse import ArgumentParser

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from exemple_formation.models import Base, FluxRSS


DB_PATH = "exemple.db"


def main():
    engine = create_engine(f"sqlite:///{DB_PATH}") 
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)

    db_session = Session()

    args = parse_args()

    ajouter_un_flux(db_session, args.url)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("url")
    return parser.parse_args()


def ajouter_un_flux(db_session, url):
    try:
        flux = FluxRSS(url=url)
        db_session.add(flux)
        db_session.commit()
    except IntegrityError:
        print("Ce flux existe déjà")


