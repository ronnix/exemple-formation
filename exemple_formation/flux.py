import time
from argparse import ArgumentParser

import feedparser
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
        print(time.time())
        for url in args.urls:
            ajouter_un_flux(db_session, url)
            print(time.time())
    elif args.cmd == "list":
        lister_les_flux(db_session)


def parse_args():
    parser = ArgumentParser()
   
    subparsers = parser.add_subparsers()

    cmd_add = subparsers.add_parser("add")
    cmd_add.add_argument("urls", nargs="+")
    cmd_add.set_defaults(cmd="add")

    cmd_list = subparsers.add_parser("list")
    cmd_list.set_defaults(cmd="list")

    return parser.parse_args()


def ajouter_un_flux(db_session, url):
    titre = titre_flux(url)
    flux = FluxRSS(url=url, nom=titre)
    try:
        db_session.add(flux)
        db_session.commit()
    except IntegrityError:
        print("Ce flux existe déjà")


def titre_flux(url):
    d = feedparser.parse(url)
    return d["feed"]["title"]


def lister_les_flux(db_session):
    for flux in db_session.query(FluxRSS):
        print(flux.nom, flux.url)
