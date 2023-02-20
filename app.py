from bottle import get, run, template, static_file, response, request
import sqlite3

db = sqlite3.connect('twitter.db')


@get("/")
def render_index():
    return template("index", title="Twitter")


@get("/app.css")
def _():
    return static_file("app.css", root=".")


@get("/thumbnails/<filename:re:.*\.jpg>")
def _(filename):
    return static_file(filename, root="./thumbnails")


@get("/banners/<filename:re:.*\.jpeg>")
def _(filename):
    return static_file(filename, root="./banners")


@get("/<username>")
def _(username):
    return template("profile", user=username)


run(host="127.0.0.1", port=3001, reloader=True, debug=True)  # 65535
