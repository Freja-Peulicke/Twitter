import git
from bottle import default_app, get, post, run
from bottle import get, run, template, static_file, response, request
import sqlite3

db = sqlite3.connect('twitter.db')


# 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
# https://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github.com/frej1187/twitter.git
#########################


@post('/6caaba75-aa1e-4f5d-b676-fe5c28cdfe86')
def git_update():
    repo = git.Repo('./twitter')
    origin = repo.remotes.origin
    repo.create_head('main', origin.refs.main).set_tracking_branch(
        origin.refs.main).checkout()
    origin.pull()
    return ""


@get("/")
def _():
    return "Two"


"""@get("/")
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
"""

##############################
# Run in AWS
try:
    import production
    print("Server running on AWS")
    application = default_app()
# Run in local computer
except Exception as ex:
    print("Server running locally")
    run(host="127.0.0.1", port=3001, debug=True, reloader=True)
##############################

# run(host="127.0.0.1", port=3001, reloader=True, debug=True)  # 65535
