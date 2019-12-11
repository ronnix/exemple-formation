from flask import Flask, render_template, request

from exemple_formation.models import Article, FluxRSS, init_db

app = Flask(__name__)

Session = init_db(f"sqlite:///exemple.db")

@app.route("/")
def index():
    db_session = Session()
    feeds = db_session.query(FluxRSS).order_by("nom")
    return render_template("index.html", feeds=feeds)


@app.route("/feed/<path:url>")
def liste_articles(url):
    db_session = Session()
    feed = db_session.query(FluxRSS).get(url)
    return render_template("articles.html", feed=feed)


@app.route("/article/<int:article_id>")
def contenu_article(article_id):
    db_session = Session()
    article = db_session.query(Article).get(article_id)
    return render_template("article.html", article=article)


if __name__ == '__main__':
    app.run()
