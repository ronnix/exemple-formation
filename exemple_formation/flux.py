import os
import time
from argparse import ArgumentParser
from multiprocessing import Process

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

        print(f"Processus principal: {os.getpid()}")

        processes = []
        for url in args.urls:
            # On lance un thread par URL
            t = ProcessAdder(Session, url)
            t.start()

            processes.append(t)

        # On attend que tous les processes aient fini
        for p in processes:
            p.join()

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


class ProcessAdder(Process):
    def __init__(self, Session, url):
        super().__init__()
        self.db_session = Session()
        self.url = url

    def run(self):
        # le point d'entrée du thread
        print(f"Démarrage du processus: {os.getpid()} ({os.getppid()})")
        ajouter_un_flux(self.db_session, self.url)


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


def lister_les_flux(Session):
    db_session = Session()
    for flux in db_session.query(FluxRSS):
        print(flux.nom, flux.url)
