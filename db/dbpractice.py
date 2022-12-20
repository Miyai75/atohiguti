import psycopg2

# PostgreSQLへ接続

# 外部からアクセスするURL張った
conn = psycopg2.connect("postgres://higuchi:7zqNWEyDOhkW7djquBaxbvplxdPZCV06@dpg-cdqtnv1gp3jnj83nmri0-a.singapore-postgres.render.com/atohiguchi_db_ynhs")
# PostgreSQLからデータの取得
cur = conn.cursor()
cur.execute('SELECT * FROM users;')
results = cur.fetchall()
print(results)
cur.close()

# PostgreSQLの接続を終了
conn.close()
print("finish")