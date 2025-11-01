import sqlite3
db = r'C:/MIND_MVP_BUILD/MIND_FIN_PRO/backend/mindfin.db'
con = sqlite3.connect(db); cur = con.cursor()
cur.execute('SELECT email, substr(password_hash,1,4) FROM users')
for email, prefix in cur.fetchall():
    print(email, prefix)
