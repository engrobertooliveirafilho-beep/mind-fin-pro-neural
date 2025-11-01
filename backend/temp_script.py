import sqlite3
db = r'C:/MIND_MVP_BUILD/MIND_FIN_PRO/backend/mindfin.db'
con = sqlite3.connect(db)
cur = con.cursor()
cur.execute("SELECT id, email, password_hash FROM users")
for r in cur.fetchall():
    print(r[0], r[1], r[2][:60] if r[2] else None)
