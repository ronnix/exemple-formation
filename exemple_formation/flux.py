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

    if args.cmd == "add":
        ajouter_un_flux(db_session, args.url)
    elif args.cmd == "list":
        lister_les_flux(db_session)


def parse_args():
    parser = ArgumentParser()
   
    subparsers = parser.add_subparsers()

    cmd_add = subparsers.add_parser("add")
    cmd_add.add_argument("url")
    cmd_add.set_defaults(cmd="add")

    cmd_list = subparsers.add_parser("list")
    cmd_list.set_defaults(cmd="list")

    return parser.parse_args()


def ajouter_un_flux(db_session, url):
    try:
        flux = FluxRSS(url=url)
        db_session.add(flux)
        db_session.commit()
    except IntegrityError:
        print("Ce flux existe déjà")


def lister_les_flux(db_session):
    for flux in db_session.query(FluxRSS):
        print(flux.url)
