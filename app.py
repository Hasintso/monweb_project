
import sqlite3
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "I_COM_SECRET_KEY"


# Fonction pour vérifier les identifiants dans SQLite3
def verifier_utilisateur(username, password):
    conn = sqlite3.connect("i_com.db")
    cursor = conn.cursor()

    # Cherche l'utilisateur avec le bon mot de passe
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password),
    )
    user = cursor.fetchone()

    conn.close()
    return user  # Retourne l'utilisateur si il existe, sinon None


@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if "user" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Vérification dynamique via la base de données
        if verifier_utilisateur(username, password):
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            message = "Nom d'utilisateur ou mot de passe incorrect."

    return render_template("login.html", message=message)


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
    