# Blueprint pages — routes des vues HTML (allège app.py)
from flask import render_template, send_from_directory


def register_pages(app, charger_profil):
    """Enregistre les routes des pages et assets (favicon, tests)."""

    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(".", "favicon.ico")

    @app.route("/tests/<filename>")
    def serve_test_file(filename):
        return send_from_directory("tests", filename)

    @app.route("/")
    def index():
        profil = charger_profil()
        return render_template("index.html", profil=profil)

    @app.route("/tutorial")
    def tutorial():
        return render_template("tutorial_welcome.html")

    @app.route("/terminal")
    def terminal():
        profil = charger_profil()
        return render_template("terminal.html", profil=profil)

    @app.route("/monde")
    def monde():
        profil = charger_profil()
        return render_template("monde.html", profil=profil)

    @app.route("/profil")
    def profil():
        profil = charger_profil()
        return render_template("profil.html", profil=profil)

    @app.route("/dashboard")
    def dashboard():
        profil = charger_profil()
        return render_template("dashboard.html", profil=profil)

    @app.route("/explorateur")
    def explorateur():
        profil = charger_profil()
        return render_template("explorateur.html", profil=profil)

    @app.route("/mail")
    def mail():
        profil = charger_profil()
        return render_template("mail.html", profil=profil)

    @app.route("/audio")
    def audio():
        profil = charger_profil()
        return render_template("audio.html", profil=profil)

    @app.route("/accessibility")
    def accessibility():
        profil = charger_profil()
        return render_template("accessibility_panel.html", profil=profil)

    @app.route("/leaderboard")
    def leaderboard_page():
        return render_template("leaderboard.html")

    @app.route("/skill-tree")
    def skill_tree_page():
        return render_template("skill_tree.html")

    @app.route("/technical-tutorials")
    def technical_tutorials_page():
        profil = charger_profil()
        return render_template("technical_tutorials.html", profil=profil)
