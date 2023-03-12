import datetime
import pathlib
import sqlite3

from bottle import (default_app, get, post, request, response, run,
                    static_file, template)

db = sqlite3.connect('twitter.db')


# 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
# https://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github.com/frej1187/twitter.git
#########################
#########################


try:
    import git
    import production
    web_folder = "twitter/"
# Run in local computer
except Exception as ex:
    web_folder = ""

##################################################
# ny kode med login og logout

@get("/login")
def _():
    return template("login")

##############################
@get("/logout")
def _():
    response.delete_cookie("user")
    response.status = 303
    response.set_header("Location", "/")
    return

@get("/notifications")
def _():
    response.add_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
    response.add_header("Pragma", "no-cache")
    response.add_header("Expires", 0)

    logged_in_user = request.get_cookie("user", secret="my-secret")
    if not logged_in_user:
        response.status=303
        response.set_header("Location", "/login")
        return
    else:
        response.status=303
        response.set_header("Location", "/")
        return

import bro.login
##################################################



@get("/js/<filename>")
def _(filename):
  return static_file(filename, "js")


def dict_factory(cursor, row):
    col_names = [col[0] for col in cursor.description]
    return {key: value for key, value in zip(col_names, row)}


def get_suggested_followers():
    try:
        db = sqlite3.connect(
            str(pathlib.Path(__file__).parent.resolve())+"/twitter.db")
        db.row_factory = dict_factory
        followers = db.execute(
            "SELECT * FROM users LIMIT 3").fetchall()
        return followers
    except Exception as ex:
        print(ex)
        return "error"
    finally:
        if "db" in locals():
            db.close()

# webhook git og PA


@post('/6caaba75-aa1e-4f5d-b676-fe5c28cdfe86')
def git_update():
    repo = git.Repo('./twitter')
    origin = repo.remotes.origin
    repo.create_head('main', origin.refs.main).set_tracking_branch(
        origin.refs.main).checkout()
    origin.pull()
    return ""


@get("/")
def render_index():
    response.add_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
    response.add_header("Pragma", "no-cache")
    response.add_header("Expires", 0)

    logged_in_user = request.get_cookie("user", secret="my-secret")

    db = sqlite3.connect(
        str(pathlib.Path(__file__).parent.resolve())+"/twitter.db")
    db.row_factory = dict_factory
    suggested_followers = get_suggested_followers()
    tweets = db.execute(
        "SELECT users.id AS user_id, message, image, tweets.created_at AS tweet_created_at, replies, retweets, likes, views, username, first_name, last_name FROM tweets JOIN users ON user_fk = users.id ORDER BY RANDOM() LIMIT 5").fetchall()
    return template("index", title="Twitter", suggested_followers=suggested_followers, tweets=tweets, logged_in_user=logged_in_user)


@get("/app.css")
def _():
    return static_file("app.css", root="./" + web_folder)


@get("/favicon.jpg")
def _():
    return static_file("favicon.jpg", root="./" + web_folder + "images/")


@get("/avatars/<filename:re:.*\.jpg>")
def _(filename):
    return static_file(filename, root="./" + web_folder + "images/avatars/")


@get("/banners/<filename:re:.*\.jpg>")
def _(filename):
    return static_file(filename, root="./" + web_folder + "images/banners")


@get("/tweets/<filename:re:.*\.jpg>")
def _(filename):
    return static_file(filename, root="./" + web_folder + "images/tweets")


@get("/<username>")
def _(username):
    try:
        response.add_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        response.add_header("Pragma", "no-cache")
        response.add_header("Expires", 0)

        logged_in_user = request.get_cookie("user", secret="my-secret")
        suggested_followers = get_suggested_followers()
        db = sqlite3.connect(
            str(pathlib.Path(__file__).parent.resolve())+"/twitter.db")
        db.row_factory = dict_factory
        user = db.execute(
            "SELECT * FROM users WHERE username=? COLLATE NOCASE", (username,)).fetchall()[0]
        tweets = db.execute(
            "SELECT * FROM tweets WHERE user_fk=?", (user["id"],)).fetchall()
        title = user["first_name"] + " " + user["last_name"] + \
            " (@" + user["username"] + ") / Twitter"
        return template("profile", user=user, suggested_followers=suggested_followers, tweets=tweets, title=title, logged_in_user=logged_in_user)
        # return "test"
    except Exception as ex:
        print(ex)
        return "error"
    finally:
        if "db" in locals():
            db.close()

##############################
# VIEWS
import views.tweet

##############################
# APIS
import apis.api_tweet

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
