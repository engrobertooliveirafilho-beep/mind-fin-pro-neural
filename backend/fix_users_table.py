import sqlite3, os

db = r"C:/MIND_MVP_BUILD/MIND_FIN_PRO/backend/mindfin.db"
con = sqlite3.connect(db)
cur = con.cursor()

# drop para garantir um estado limpo (a tabela estava errada)
cur.execute("DROP TABLE IF EXISTS users")

cur.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    name TEXT NOT NULL,
    bio TEXT,
    ai_profile TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

con.commit()
con.close()
print("Tabela users recriada com sucesso.")
