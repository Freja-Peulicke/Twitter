from bottle import default_app, get, post, request, response, run, static_file, template
import x
import os
import uuid
import time




#########################
#########################
#TO-DO : få styr på at uploade billeder

@post("/upload-picture")
def _():
    try:
        the_picture = request.files.get("picture")
        name, ext = os.path.splitext(the_picture.filename)
        if ext not in ( ".png", ".jpg", ".jpeg"):
            response.status = 400
            return "picture not allowed"
        picture_name = str(uuid.uuid4().hex)
        picture_name = picture_name + ext 
        the_picture.save(f"pictures/{picture_name}")
        return "picture uploaded"
    except Exception as e:
        print(e)
    finally:
        pass


### for at undgå at uploade de statiske filer, er ikke noget santiago har. 
try:
    import production
    import git
    web_folder = "twitter/"
# Run in local computer
except Exception as ex:
    web_folder = ""


    # webhook git og PA
@post('/6caaba75-aa1e-4f5d-b676-fe5c28cdfe86')
def git_update():
    repo = git.Repo('./twitter')
    origin = repo.remotes.origin
    if not 'main' in repo.heads:
        repo.create_head('main', origin.refs.main).set_tracking_branch(
            origin.refs.main).checkout()
    origin.pull()
    return ""


##################################################
# flyttes til views/index.py
@get("/")
def render_index():
    try:
        x.disable_cache()

        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)

        db = x.db()
        cur = db.cursor()
        if logged_in_user:
            suggested_followers = get_suggested_followers()
            tweets = cur.execute("SELECT users.*, tweets.*, CASE WHEN likes.like_user_fk = ? THEN 1 ELSE 0 END AS user_liked FROM tweets JOIN users ON tweet_user_fk = user_id LEFT JOIN likes ON tweets.tweet_id = likes.like_tweet_fk WHERE tweets.tweet_id IN (SELECT like_tweet_fk FROM likes WHERE like_user_fk = ?) OR likes.like_user_fk IS NULL ORDER BY tweet_created_at DESC LIMIT 15", (logged_in_user["user_id"],logged_in_user["user_id"], )).fetchall()
        else:
            suggested_followers = []
            tweets = cur.execute("SELECT users.*, tweets.* FROM tweets JOIN users ON tweet_user_fk = user_id ORDER BY tweet_created_at DESC LIMIT 15").fetchall()

        retweet_ids = []
        for tweet in tweets:
            tweet_retweet_fk = tweet["tweet_retweet_fk"]
            if tweet_retweet_fk:
                retweet_ids.append(str(tweet_retweet_fk))

        placeholders = ', '.join('?' for _ in retweet_ids)

        retweets = cur.execute("SELECT users.*, tweets.* FROM tweets JOIN users ON tweet_user_fk = user_id WHERE tweet_id IN ({})".format(placeholders), retweet_ids).fetchall()

        retweets = {retweet['tweet_id']: retweet for retweet in retweets}  # Assigning sorted retweets to the same variable

        return template("index", title="Twitter", suggested_followers=suggested_followers, tweets=tweets, logged_in_user=logged_in_user, retweets=retweets)
    except Exception as ex:
        if 'db' in locals(): db.rollback()
        print(ex)
        return "error"
    finally:
        if "db" in locals():
            db.close()

# flyttes til views/profile.py
@get("/<username>")
def _(username):
    try:
        x.disable_cache()
 
        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)

        db = x.db()
        cur = db.cursor()
        user = cur.execute(
            "SELECT * FROM users WHERE user_name=? COLLATE NOCASE", (username,)).fetchall()[0]
        
        if logged_in_user:
            suggested_followers = get_suggested_followers()
            tweets = cur.execute(
                "SELECT tweets.*, CASE WHEN likes.like_user_fk = ? THEN 1 ELSE 0 END AS user_liked FROM tweets LEFT JOIN likes ON tweets.tweet_id = likes.like_tweet_fk WHERE tweets.tweet_user_fk = ? AND tweets.tweet_id IN (SELECT like_tweet_fk FROM likes WHERE like_user_fk = ?) OR likes.like_user_fk IS NULL AND tweets.tweet_user_fk = ? ORDER BY tweets.tweet_created_at DESC",(logged_in_user["user_id"], user["user_id"], logged_in_user["user_id"], user["user_id"],)
            ).fetchall()
        else:
            suggested_followers = []
            tweets = cur.execute("SELECT *, 0 AS user_liked FROM tweets WHERE tweet_user_fk = ?", (user["user_id"],)).fetchall()        

        retweet_ids = []
        for tweet in tweets:
            tweet_retweet_fk = tweet["tweet_retweet_fk"]
            if tweet_retweet_fk:
                retweet_ids.append(str(tweet_retweet_fk))

        placeholders = ', '.join('?' for _ in retweet_ids)

        retweets = cur.execute("SELECT users.*, tweets.* FROM tweets JOIN users ON tweet_user_fk = user_id WHERE tweet_id IN ({})".format(placeholders), retweet_ids).fetchall()

        retweets = {retweet['tweet_id']: retweet for retweet in retweets}  # Assigning sorted retweets to the same variable

        title = user["user_first_name"] + " " + user["user_last_name"] + \
            " (@" + user["user_name"] + ") / Twitter"
        followed = False
        if logged_in_user:
            follow_data = cur.execute(
                "SELECT * FROM followers WHERE follower_fk = ? AND followee_fk = ?", (logged_in_user["user_id"], user["user_id"],)).fetchone()
            if follow_data:
                followed = True
        return template("profile", user=user, suggested_followers=suggested_followers, tweets=tweets, title=title, logged_in_user=logged_in_user, followed=followed, retweets=retweets)
        
    except Exception as ex:
        if 'db' in locals(): db.rollback()
        print(ex)
        return "error"
    finally:
        if "db" in locals():
            db.close()
###############################################################
@get("/tweet/<tweet_id>")
def _(tweet_id):
    try:
        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)
        
        db = x.db()
        cur = db.cursor()
        if logged_in_user:
            tweet = cur.execute("SELECT tweets.*, users.*, CASE WHEN likes.like_user_fk = ? AND likes.like_tweet_fk = ? THEN 1 ELSE 0 END AS user_liked FROM tweets LEFT JOIN likes ON tweets.tweet_id = likes.like_tweet_fk JOIN users ON tweets.tweet_user_fk = users.user_id WHERE tweets.tweet_id = ?", (logged_in_user["user_id"], tweet_id, tweet_id,)).fetchone()
            comments = cur.execute("SELECT comments.*, users.*, CASE WHEN likes.like_user_fk = ? AND likes.like_comment_fk = comments.comment_id THEN 1 ELSE 0 END AS user_liked FROM comments LEFT JOIN likes ON comments.comment_id = likes.like_comment_fk JOIN users ON comments.comment_user_fk = users.user_id WHERE comments.comment_tweet_fk = ? ORDER BY comments.comment_created_at DESC", (logged_in_user["user_id"], tweet_id,)).fetchall()
        else:
            tweet = cur.execute("SELECT tweets.*, users.*, 0 AS user_liked FROM tweets JOIN users ON tweets.tweet_user_fk = users.user_id WHERE tweets.tweet_id = ?", (tweet_id,)).fetchone()
            comments = cur.execute("SELECT comments.*, users.*, 0 AS user_liked FROM comments JOIN users ON comments.comment_user_fk = users.user_id WHERE comments.comment_tweet_fk = ? ORDER BY comments.comment_created_at DESC", (tweet_id,)).fetchall()        
        if logged_in_user:
            suggested_followers = get_suggested_followers()
        else:
            suggested_followers = []
        return template("tweet",logged_in_user=logged_in_user, suggested_followers=suggested_followers, tweet=tweet, comments=comments)
    except Exception as ex:
        if 'db' in locals(): db.rollback()
        print(ex)
        return "error"
    finally:
        if "db" in locals():
            db.close()

###############################################################
@get("/signup")
def _():
    x.disable_cache()
    user = request.get_cookie("user", secret=x.COOKIE_SECRET)
    if user:
        response.status = 303
        response.set_header("Location", f"/{user['user_name']}")
        return
    return template("signup") 

###############################################################

@get("/activate/<user_id>")
def _(user_id):
    try:
        user_activated_at = int(time.time())
        db = x.db()
        cur = db.cursor()
        total_rows_updated = cur.execute("UPDATE users SET user_activated_at = ? WHERE user_id = ? AND user_activated_at = 0", (user_activated_at, user_id,)).rowcount
        print(user_activated_at)
        print(user_id)
        if total_rows_updated != 1: raise Exception("Please, try again")
        db.commit()
        return template("activate", status="succes")
    except Exception as ex:
        if 'db' in locals(): db.rollback()
        print(ex)
        response.status = 400
        return template("activate", status="error")
    finally:
        if "db" in locals():
            db.close()
###############################################################

# ny kode med login og logout, skiftes ud med ny side i views/login.py
@get("/login")
def _():
    return template("login")


@get("/forgot-password")
def _():
    return template("forgot-password")


@get("/reset-password/<user_id>")
def _(user_id):
    return template("reset-password", user_id=user_id, web_folder=web_folder)



##################################################

##################################################
@get("/gold")
def render_index():
    try:
        x.disable_cache()

        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)

        if logged_in_user:
            suggested_followers = get_suggested_followers()
        else:
            suggested_followers = []

        return template("gold", title="Gold / Twitter", suggested_followers=suggested_followers, logged_in_user=logged_in_user)
    except Exception as ex:
        print(ex)
        return "error"
    finally:
        if "db" in locals():
            db.close()

################################################## 
@get("/admin")
def _():
    try:
        x.disable_cache()
        
        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)

        if not logged_in_user or logged_in_user["user_admin"] == 0:
            response.status = 303
            response.set_header("Location", "/")
            return

        db = x.db()
        cur = db.cursor()

        users = cur.execute("SELECT *, DATETIME(user_blocked_until, 'unixepoch') as user_blocked_until_formated FROM users").fetchall()

        return template("admin", suggested_followers=[], logged_in_user=logged_in_user, users=users, current_time=time.time())
    except Exception as ex:
        if 'db' in locals(): db.rollback()
        print(ex)
        return "error"
    finally:
        if "db" in locals():
            db.close()

################################################## 
# Henter 3 rækker fra vores users table i databasen, som vi bruger til suggested followers
def get_suggested_followers():
    try:
        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)
        db = x.db()
        cur = db.cursor()
        followers = cur.execute(
            "SELECT * FROM users WHERE user_id != ? ORDER BY RANDOM() LIMIT 3", (logged_in_user["user_id"],)).fetchall()
        return followers
    except Exception as ex:
        if 'db' in locals(): db.rollback()
        print(ex)
        return "error"
    finally:
        if "db" in locals():
            db.close()



""" @get("/test")
def _():
    for x in range(100):
        print("name")
    return "X"
 """
@get("/test")
def _():
    name = "Freja"
    return template("test", name = name)

##################################################
@get("/app.css")
def _():
    return static_file("app.css", root="./" + web_folder)

@get("/favicon.jpg")
def _():
    return static_file("favicon.jpg", root="./" + web_folder + "images/")

@get("/js/<filename>")
def _(filename):
    return static_file(filename, root="./" + web_folder + "js/")

@get("/avatars/<filename:re:.*\.(jpg|jpeg|png)>")
def _(filename):
    return static_file(filename, root="./" + web_folder + "images/avatars/")

@get("/banners/<filename:re:.*\.(jpg|jpeg|png)>")
def _(filename):
    return static_file(filename, root="./" + web_folder + "images/banners")

@get("/tweets/<filename:re:.*\.(jpg|jpeg|png)>")
def _(filename):
    return static_file(filename, root="./" + web_folder + "images/tweets")

##############################

##############################
# VIEWS
#import views.tweet

##############################
# APIS
import apis.api_tweet
import apis.api_sign_up
import apis.api_login
import apis.api_like
import apis.api_unlike
import apis.api_search
import apis.api_follow
import apis.api_unfollow
import apis.api_gold
import apis.api_gold_verify
import apis.api_edit_profile
import apis.api_forgot_password 
import apis.api_reset_password
import apis.api_comment
import apis.api_delete
import apis.api_retweet
import apis.api_admin_block_unblock_user
import apis.api_admin_delete_user

##############################
#Bridges
import bridge.logout
import bridge.delete_user

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