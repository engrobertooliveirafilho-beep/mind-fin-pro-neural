import sqlite3
db = r'C:/MIND_MVP_BUILD/MIND_FIN_PRO/backend/mindfin.db'
con = sqlite3.connect(db)
cur = con.cursor()
cur.execute('SELECT COUNT(*) FROM users')
print('Total de usuários:', cur.fetchone()[0])
