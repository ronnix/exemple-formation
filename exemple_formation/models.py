"""
Modéliser des flux RSS.

- FluxRSS
    - url
    - nom

- Article
    - date de publication
    - titre
    - auteur
    - contenu
    - url
"""

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FluxRSS(Base):
    __tablename__ = "flux_rss"

    url = Column(String, primary_key=True)
    nom = Column(String)
    

class Article(Base):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True)
    date = Column(String)
    titre = Column(String)
    auteur = Column(String)
    contenu = Column(String)
    article_url = Column(String)

    flux_url = Column(String, ForeignKey("flux_rss.url"))


def init_db(filename):
    engine = create_engine(f"sqlite:///{filename}")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session
