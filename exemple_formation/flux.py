import asyncio
import os
import time
from argparse import ArgumentParser

import aiohttp
import feedparser
from sqlalchemy.exc import IntegrityError

from exemple_formation.models import Article, FluxRSS, init_db


DB_URL = "sqlite:///exemple.db"


def main():
    Session = init_db(DB_URL)

    args = parse_args()

    if args.cmd == "add":
        initial = time.time()

        feeds = asyncio.run(parse_all_flux(args.urls))

        for url, feed in feeds.items():
            ajouter_un_flux(Session, url, titre_flux(feed))
            for entry in feed["entries"]:
                ajouter_un_article(Session, entry, url)

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


def ajouter_un_article(Session, entry, flux_url):
    db_session = Session()
    article = Article(
        date=entry.published,
        titre=entry.title,
        auteur=getattr(entry, "author", None),
        contenu=entry.description,  # TODO: clean HTML
        article_url=entry.link,
        flux_url=flux_url,
    )
    try:
        db_session.add(article)
        db_session.commit()
    except IntegrityError:
        print("Cet article existe déjà")


async def parse_all_flux(urls):
    parsed = {}
    for url in urls:
        parsed[url] = await parse_flux(url)
    return parsed


async def parse_flux(url):
    contenu = await récupération(url)
    return feedparser.parse(contenu)


def titre_flux(d):
    return d["feed"]["title"]


async def récupération(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


def lister_les_flux(Session):
    db_session = Session()
    for flux in db_session.query(FluxRSS):
        print(flux.nom, flux.url)
