
import sqlite3

# Crée le fichier de la base de données
conn = sqlite3.connect("i_com.db")
cursor = conn.cursor()

# Crée la table des utilisateurs
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
"""
)

# Ajoute l'administrateur par défaut (si il n'existe pas déjà)
try:
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("admin", "123456"),
    )
    conn.commit()
    print("Base de données créée avec succès ! L'utilisateur 'admin' a été ajouté.")
except sqlite3.IntegrityError:
    print("La base de données existe déjà.")

conn.close()
