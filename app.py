
import os
import sqlite3
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "I_COM_SECRET_KEY"

# --- ADAPTATION AUTOMATIQUE ANDROID / RENDER ---
# Si le dossier /tmp existe (sur Render), on l'utilise, sinon on crée le fichier localement (sur Android)
if os.path.exists("/tmp"):
    DB_PATH = "/tmp/i_com.db"
else:
    DB_PATH = "i_com.db"


# --- CRÉATION AUTOMATIQUE DE LA BASE DE DONNÉES ---
def initialiser_base_en_ligne():
    conn = sqlite3.connect(DB_PATH)
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
        pass  # L'administrateur existe déjà
    conn.close()


# Lancement automatique
initialiser_base_en_ligne()


# --- VÉRIFICATION DES IDENTIFIANTS ---
def verifier_utilisateur(username, password):
    conn = sqlite3.connect(DB_PATH)
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
    app.run(host="0.0.0.0", port=5000, debug=False)
    
