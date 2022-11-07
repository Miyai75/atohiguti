import psycopg2

# 設定値
users = 'fyllxwodgdeqbx'     # DBにアクセスするユーザー名(適宜変更)
dbnames = 'd862de1h1e3l58'   # 接続するデータベース名(適宜変更)
passwords = '90eca05f392cee31b0b9d06a7a6715d7bd89527f10cb666569a82351e3483720' # DBにアクセスするユーザーのパスワード(適宜変更)
host = "ec2-52-200-5-135.compute-1.amazonaws.com"      # DBが稼働しているホスト名(適宜変更)
port = 5432        # DBが稼働しているポート番号(適宜変更)

# PostgreSQLへ接続
conn = psycopg2.connect("user=" + users +" dbname=" + dbnames +" password=" + passwords, host=host, port=port)

# PostgreSQLからデータの取得
cur = conn.cursor()
cur.execute('SELECT * FROM users;')
results = cur.fetchall()
print(results)
cur.close()

# PostgreSQLの接続を終了
conn.close()
print("finish")