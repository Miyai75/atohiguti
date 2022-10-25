import http.server
import socketserver

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()


# 実行したらこのリンクをクリック → http://localhost:8000

"""
これは一旦テストサーバー内で動くかどうか確認するためのサーバ立ち上げプログラムです
ここでエラーになったらプログラミング間違い
ここでエラーにならずにheroku側でエラーになったらherokuエラーだと思ってください
"""