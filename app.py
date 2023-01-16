from flask import Flask, request, render_template, session, redirect, url_for,flash
from db import dbmodule as db
from datetime import timedelta 

app = Flask(__name__)
app.secret_key = 'atohiguchi' 
app.permanent_session_lifetime = timedelta(days=1)

# 実行したらこのリンクをクリック → http://127.0.0.1:5000/

"""
これは一旦テストサーバー内で動くかどうか確認するためのサーバ立ち上げプログラムです
ここでエラーになったらプログラミングやルーティング間違い
ここでエラーにならずにheroku側でエラーになったらherokuエラーだと思ってください
"""

user = db.DBmoduleClass("loginID","password")

# ホーム画面
@app.route('/', methods=['GET', 'POST'])
def home():
    global user
    print(session)
    if "login_id" in session:
        user.user_info = user.userFindDB(session["login_id"])
        print(f"ホーム画面で{user.user_info}")
        return render_template(
            'higuchi.html',
            name = session["login_id"],
            date = user.user_info[0][6].strftime('%Y-%m-%d %H:%M'),
            imgname = user.user_info[0][4])        
    return render_template('loginform2.html')

# ログインするやつ
@app.route('/login', methods=['GET', 'POST'])
def login():
    global user
    if request.method == "POST":
        loginID = request.form['loginID']
        password = request.form['password']
        if loginID == "" or password == "":
            alart = "全ての項目を埋めてください"
            return render_template('loginform2.html', alart = alart)

        print("postできました")
        # データベースからデータを検索
        user = db.DBmoduleClass(loginID,password)
        result = user.user_info

        # idが無かったり、パスワードが会ってなかったら戻る
        if result == [] or result[0][3] != password:
            alart = "loginIDまたはパスワードが間違っています"
            return render_template('loginform2.html', alart = alart)
        
        session.permanent = True 
        session["login_id"] = loginID #sessionにuser情報を保存
        user.userUpdateDB(0, session["login_id"])
        return redirect(url_for("home")) #homeメソッドに遷移
    else:
        if "login_id" in session:
            return redirect(url_for("home"))
        

# ログアウトするやつ
@app.route('/logout')
def logout():
    global user
    user.userUpdateDB(1, session["login_id"])
    session.pop('id',None)
    session.clear()
    return redirect("/")

# 新規登録する奴
@app.route('/newok', methods=['GET', 'POST'])
def newok():
    global user
    loginID = request.form['loginID']
    mailaddres = request.form['mailaddres']
    password = request.form['password']
    if loginID == "" or mailaddres == "" or password == "":
        alart = "全ての項目を埋めてください"
        return render_template('newuser2.html', alart = alart)

    print(loginID,mailaddres,password)
    # データベースからデータを検索
    user = db.DBmoduleClass(loginID,password,mailaddres)
    result = user.user_info
    # login_id検索でヒットしてしまった時
    if result != []:
        alart = "すでに使われてるlogin_idです。"
        return render_template('newuser2.html', alart = alart)
    print("db行けました")
    #データベースに追加
    user.userAddDB()     
    return render_template('kakuninn.html', result = f"loginID:{loginID}\nMailaddres:{mailaddres}\nで登録しました！")
    

# 新規登録画面
@app.route('/newuser', methods=['GET', 'POST'])
def newuser():
    return render_template('newuser2.html')

# ガチャ画面
@app.route('/gatya/')
def gatya():
    if "login_id" in session:
        return render_template('gatya.html')
    else:
        return redirect(url_for("home"))

# ガチャリザルト画面
@app.route('/gatya_result/', methods=['POST'])
def gatya_result():
    global user
    if "login_id" in session:
        result = user.itemlogFindDB(session["login_id"])
        # 全て取得しているとき
        if result[0] == "a":
            allget = result[1]
        else:
            allget = ""
            user.itemlogAddDB(user.user_info[0][0],result[0])
        print(result)
        return render_template('gatya_result.html', result = result[2], allget = allget)
    else:
        print("mawattemasu")
        return redirect(url_for("home"))

# レッスンセレクト画面
@app.route('/lessonselect')
def gameplay():
    global user
    if "login_id" in session:
        user.user_info = user.userFindDB(session["login_id"])
        print(f"ホーム画面で{user.user_info}")
        return render_template(
            'higuchi-eikaiwa.html',
            name = session["login_id"],
            date = user.user_info[0][6].strftime('%Y-%m-%d %H:%M'),
            imgname = user.user_info[0][4])
    return render_template('loginform2.html')

#英会話画面
@app.route('/lesson')
def lesson():
    global user
    if "login_id" in session:
        user.user_info = user.userFindDB(session["login_id"])
        print(f"ホーム画面で{user.user_info}")
        return render_template(
            'higuchi-eikaiwa-lesson.html',
            name = session["login_id"],
            date = user.user_info[0][6].strftime('%Y-%m-%d %H:%M'),
            imgname = user.user_info[0][4])
    return render_template('loginform2.html')

# 着せ替え画面
@app.route('/dressup/',methods=['GET','POST'])
def dressup():
    global user
    if "login_id" in session:
        itemnamelist=[]
        user.user_info = user.userFindDB(session["login_id"])
        # 自分の持ってるitemidを検索
        item = user.itemlogFindDB(session["login_id"],False)
        print(item)
        # itemidをnameに変換
        for id in item:
            print(f"kokomitene:{id}")
            itemnamelist.append(user.itemFindDB(id)[0][0])
        print(itemnamelist)
        imgname = user.user_info[0][4]
        return render_template(
            'higuchi-kisekae.html',
            imgname=imgname,
            itemnamelist = itemnamelist,
            name = session["login_id"],
            date = user.user_info[0][6].strftime('%Y-%m-%d %H:%M'))
    return render_template('loginform2.html')

# 着せ替え決定したら
@app.route('/dressupok/',methods=['POST'])
def dressupok():
    global user
    if "login_id" in session:
        itemnamelist=[]
        radio = request.form['radio']
        # 自分の持ってるitemidを検索
        item = user.itemlogFindDB(session["login_id"],False)
        print(item)
        # itemidをnameに変換
        for id in item:
            print(f"kokomitene:{id}")
            itemnamelist.append(user.itemFindDB(id)[0][0])
        print(itemnamelist)

        # 持ってるアイテムだったらそれに変更
        if radio in itemnamelist:
            user.userimgUpdateDB(session["login_id"],radio)
            flash(f"{radio}樋口に変更しました！",'ok')
        else:
            flash("まだ取得していません！！",'ng')

        # 今のimgを反映
        user.user_info = user.userFindDB(session["login_id"])
        imgname = user.user_info[0][4]
        kousin = ""
        print(imgname)
        print(radio)
    return render_template(
        'higuchi-kisekae.html',
        imgname=imgname,
        kousin=kousin, 
        itemnamelist=itemnamelist,
        name = session["login_id"],
        date = user.user_info[0][6].strftime('%Y-%m-%d %H:%M'))




if __name__ == '__main__':
    app.run()