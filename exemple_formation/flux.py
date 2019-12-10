import asyncio
import os
import time
from argparse import ArgumentParser

import aiohttp
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

        titres = asyncio.run(titres_flux(args.urls))

        for url, titre in titres.items():
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


async def titres_flux(urls):
    titres = {}
    for url in urls:
        titres[url] = await titre_flux(url)
    return titres


async def titre_flux(url):
    contenu = await récupération(url)
    d = feedparser.parse(contenu)
    return d["feed"]["title"]


async def récupération(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


def lister_les_flux(Session):
    db_session = Session()
    for flux in db_session.query(FluxRSS):
        print(flux.nom, flux.url)
