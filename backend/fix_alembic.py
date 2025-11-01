import sqlite3, sys
db = r"C:\MIND_MVP_BUILD\MIND_FIN_PRO\backend\mindfin.db"
con = sqlite3.connect(db)
cur = con.cursor()
cur.execute("SELECT version_num FROM alembic_version")
row = cur.fetchone()
print("ANTES:", row)
cur.execute("UPDATE alembic_version SET version_num = '0001_manual'")
con.commit()
cur.execute("SELECT version_num FROM alembic_version")
print("DEPOIS:", cur.fetchone())
con.close()
