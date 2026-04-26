"""Routes HTML — 4 pages : accueil, jeu, profil, leaderboard."""

from flask import render_template, send_from_directory, url_for


def register_pages(app) -> None:

    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory("static", "favicon.ico", mimetype="image/x-icon")

    @app.route("/")
    def index():
        return render_template(
            "index.html", canonical_url=url_for("index", _external=True)
        )

    @app.route("/game")
    def game():
        return render_template(
            "game.html", canonical_url=url_for("game", _external=True)
        )

    @app.route("/profil")
    def profil():
        return render_template("profil.html")

    @app.route("/leaderboard")
    def leaderboard():
        return render_template("leaderboard.html")
