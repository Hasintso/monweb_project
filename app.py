
import sqlite3
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "I_COM_SECRET_KEY"


# --- CRÉATION AUTOMATIQUE DE LA BASE DE DONNÉES SUR RENDER ---
def initialiser_base_en_ligne():
    conn = sqlite3.connect("i_com.db")
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """
    )
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", "123456"),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # L'administrateur existe déjà, aucun problème
    conn.close()


# On exécute la création automatique au démarrage du serveur
initialiser_base_en_ligne()


# --- VÉRIFICATION DES IDENTIFIANTS ---
def verifier_utilisateur(username, password):
    conn = sqlite3.connect("i_com.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password),
    )
    user = cursor.fetchone()
    conn.close()
    return user


# --- LES ROUTES DE VOTRE SITE ---
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
    # debug=False obligatoire pour éviter le crash sur Android et Render
    app.run(host="0.0.0.0", port=5000, debug=False)
