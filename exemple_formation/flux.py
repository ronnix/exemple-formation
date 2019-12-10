import os
import time
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from threading import get_ident

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

    args = parse_args()

    if args.cmd == "add":
        initial = time.time()

        print(f"Thread principal: {os.getpid()} / {hex(get_ident())}")

        urls = args.urls

        with ThreadPoolExecutor(max_workers=8) as pool:
            for url, titre in zip(urls, pool.map(titre_flux, urls)):
                ajouter_un_flux(Session, url, titre)

        print(time.time() - initial)

    elif args.cmd == "list":
        lister_les_flux(Session)


def parse_args():
    parser = ArgumentParser()
   
    subparsers = parser.add_subparsers()

    cmd_add = subparsers.add_parser("add")
    cmd_add.add_argument("urls", nargs="+")
    cmd_add.set_defaults(cmd="add")

    cmd_list = subparsers.add_parser("list")
    cmd_list.set_defaults(cmd="list")

    return parser.parse_args()


def ajouter_un_flux(Session, url, titre):
    db_session = Session()
    flux = FluxRSS(url=url, nom=titre)
    try:
        db_session.add(flux)
        db_session.commit()
    except IntegrityError:
        print("Ce flux existe déjà")


def titre_flux(url):
    print(f"Thread worker: {os.getpid()} / {hex(get_ident())}")
    d = feedparser.parse(url)
    return d["feed"]["title"]


def lister_les_flux(Session):
    db_session = Session()
    for flux in db_session.query(FluxRSS):
        print(flux.nom, flux.url)
