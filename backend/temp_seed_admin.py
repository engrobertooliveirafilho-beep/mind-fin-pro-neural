from passlib.hash import bcrypt
import sqlite3

db = r'C:/MIND_MVP_BUILD/MIND_FIN_PRO/backend/mindfin.db'
con = sqlite3.connect(db)
cur = con.cursor()

name  = 'Admin'
email = 'admin@mind.com'
pwd   = '123456'

hashed = bcrypt.hash(pwd)
cur.execute('INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
            (name, email, hashed))
con.commit()
print('Usuário criado com hash:', hashed[:30] + '...')
