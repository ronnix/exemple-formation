from flask import Flask, render_template

from exemple_formation.models import FluxRSS, init_db

app = Flask(__name__)


@app.route("/")
def index():
    Session = init_db(f"sqlite:///exemple.db")
    db_session = Session()
    feeds = db_session.query(FluxRSS).order_by("nom")
    return render_template("index.html", feeds=feeds)


if __name__ == '__main__':
    app.run()