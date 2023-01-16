import psycopg2
import json
from datetime import datetime
print(datetime.now().strftime('%Y-%m-%d %H:%M'))
class DBmoduleClass:
    user_column = ["id", "login_id", "mailaddress", "password","icon_img","star_point","pre_logintime","post_logintime"]
    json_path = 'json/user_data.json'
    # コンストラクタ（初期化）
    def __init__(self, login_id, password, mailaddress =""):
        self.login_id = login_id
        self.mail_add = mailaddress
        self.password = password
        self.user_info = self.userFindDB()
        print("初期化完了")

    # データベースと接続
    def getConnection(self):
        return  psycopg2.connect("postgres://higuchi:7zqNWEyDOhkW7djquBaxbvplxdPZCV06@dpg-cdqtnv1gp3jnj83nmri0-a.singapore-postgres.render.com/atohiguchi_db_ynhs")

    # データベースから該当するデータを受け取る(ユーザーテーブル)  
    def userFindDB(self, login_id = ""):
        print("検索開始")
        if login_id != "":
            self.login_id = login_id
        sql_1 = f"SELECT * FROM users WHERE login_id = '{self.login_id}';"

        # データベースに接続してsql文で検索
        with self.getConnection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql_1)
                rows = cur.fetchall()

        print("検索完了")
        print(f"検索結果：{rows}")

        self.user_info = rows
        return rows

    # データ追加
    def userAddDB(self):
        print("検索開始")
        sql_1 = f"INSERT INTO users(login_id, mailaddress, password, icon_img, star_point, pre_logintime, post_logintime)VALUES('{self.login_id}','{self.mail_add}', '{self.password}', 'higuchi.png', 0, '{datetime.now()}', '{datetime.now()}');"
        # データベースに接続してsql文で検索
        with self.getConnection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql_1)

        print("追加完了")
        user_id = self.userFindDB(self.login_id)[0][0]
        self.itemlogAddDB(user_id,1)
        
        return "追加完了"

    # 時間データ更新
    def userUpdateDB(self, sqlnum, login_id):
        print("アップデート開始")
        sqls =[]
        # ログインするとき
        sqls.append(f"UPDATE users SET post_logintime = '{datetime.now()}' WHERE login_id = '{login_id}';")
        # ログアウトするとき
        sqls.append (f"UPDATE users SET pre_logintime = post_logintime WHERE login_id = '{login_id}';")
        # データベースに接続してsql文で検索
        with self.getConnection() as conn:
            with conn.cursor() as cur:
                cur.execute(sqls[sqlnum])

        print("アップデート完了")
        
        return "追加完了"

    # user画像データ更新
    def userimgUpdateDB(self, login_id, radiovalue):
        print("検索開始")
        sql_1 = f"UPDATE users SET icon_img = '{radiovalue}.png' where login_id ='{login_id}';"
        # データベースに接続してsql文で検索
        with self.getConnection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql_1)
        
        return "追加完了"

    #items検索
    def itemFindDB(self, item_id):
        print("検索開始")
        sql_1 = f"Select name from items where id = {int(item_id)};"
        # データベースに接続してsql文で検索
        with self.getConnection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql_1)
                name = cur.fetchall()
        
        return name
    
    # データベースから該当するデータを受け取る(ガチャテーブル)  
    def itemlogFindDB(self, user_info, isgatya=True ):
        print("itemlog検索開始")
        print(user_info)
        print(self.user_info)
        if self.user_info == []:
            self.user_info = self.userFindDB(user_info)
            print(self.user_info)

        findsql = f"SELECT item_id FROM item_get_logs WHERE user_id = '{self.user_info[0][0]}';"
        itemnumsql = "SELECT COUNT(*) FROM items; "
        getsql  = "SELECT * FROM items ORDER BY random() LIMIT 1;"
        log_result = []
        # データベースに接続してsql文で検索
        with self.getConnection() as conn:
            with conn.cursor() as cur:
                # itemlogテーブルから検索
                cur.execute(findsql)
                resultrows = cur.fetchall()
                for item in resultrows:
                    log_result.append(item[0])
                print("itemlog検索完了")
                print(f"itemlog検索結果：{log_result}")

                # ガチャ機能の時
                if isgatya:
                    # 現時点でのitem数を取得
                    cur.execute(itemnumsql)
                    itemnum = cur.fetchall()[0][0]
                    # log_result = [1,2,3,4]

                    # 全て取得しているとき
                    if len(log_result) == itemnum:
                        print("ALL COMPLETE!!")
                        return ["a","全て取得済み","gatya.png"]
                    else:
                        # ランダムにアイテムを取得
                        cur.execute(getsql)
                        getrow = list(cur.fetchall()[0])
                        print(f"ガチャ結果:{getrow}")
                        # もしすでに持っていたら無くなるまで回す
                        while getrow[0] in log_result:
                            cur.execute(getsql)
                            getrow = list(cur.fetchall()[0])
                            print(f"ガチャ結果:{getrow}")
                        
                        return getrow
        return log_result

    # itemlogデータ追加
    def itemlogAddDB(self, user_id, item_id):
        print("データログ追加開始")
        sql_1 = f"INSERT INTO item_get_logs(user_id, item_id, timestamp)VALUES('{user_id}','{item_id}', '{datetime.now()}');"

        # データベースに接続してsql文で検索
        with self.getConnection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql_1)

        print("ログ追加完了")
        
        return "ログ完了"
# a = DBmoduleClass("tanaka","tanaka1111","aaa@example.com")
# result = a.itemlogFindDB(False)
# print(result)