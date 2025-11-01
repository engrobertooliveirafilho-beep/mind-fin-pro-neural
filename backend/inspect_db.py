import sqlite3
db = r"C:/MIND_MVP_BUILD/MIND_FIN_PRO/backend/mindfin.db"
con = sqlite3.connect(db)
cur = con.cursor()
print("DB file:", db)

cur.execute("PRAGMA table_info(users)")
cols = [(r[1], r[2]) for r in cur.fetchall()]
print("users columns:", cols)

cur.execute("SELECT COUNT(*) FROM users")
print("users rows:", cur.fetchone()[0])
