from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()


# 実行したらこのリンクをクリック → http://127.0.0.1:5000/

"""
これは一旦テストサーバー内で動くかどうか確認するためのサーバ立ち上げプログラムです
ここでエラーになったらプログラミングやルーティング間違い
ここでエラーにならずにheroku側でエラーになったらherokuエラーだと思ってください
"""