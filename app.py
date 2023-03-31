from bottle import default_app, get, post, request, response, run, static_file, template
import x
import os
import uuid


# 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

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
        suggested_followers = get_suggested_followers()
        tweets = db.execute(
            "SELECT user_id, tweet_message, tweet_image, tweet_created_at, tweet_replies, tweet_retweets, tweet_likes, tweet_views, user_name, user_first_name, user_last_name FROM tweets JOIN users ON tweet_user_fk = user_id ORDER BY RANDOM() LIMIT 5").fetchall()
        return template("index", title="Twitter", suggested_followers=suggested_followers, tweets=tweets, logged_in_user=logged_in_user)
    except Exception as ex:
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
        suggested_followers = get_suggested_followers()
        db = x.db()
        user = db.execute(
            "SELECT * FROM users WHERE user_name=? COLLATE NOCASE", (username,)).fetchall()[0]
        tweets = db.execute(
            "SELECT * FROM tweets WHERE tweet_user_fk=? ORDER BY tweet_created_at DESC", (user["user_id"],)).fetchall()
        title = user["user_first_name"] + " " + user["user_last_name"] + \
            " (@" + user["user_name"] + ") / Twitter"
        return template("profile", user=user, suggested_followers=suggested_followers, tweets=tweets, title=title, logged_in_user=logged_in_user)
        # return "test"
    except Exception as ex:
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
    return template("sign_up") 

###############################################################

# ny kode med login og logout, skiftes ud med ny side i views/login.py
@get("/login")
def _():
    return template("login")

# Skal blive her fordi den ikke returnere et template/view
@get("/logout")
def _():
    response.delete_cookie("user")
    response.status = 303
    response.set_header("Location", "/")
    return
##################################################


# Henter 3 rækker fra vores users table i databasen, som vi bruger til suggested followers
def get_suggested_followers():
    try:
        db = x.db()
        followers = db.execute(
            "SELECT * FROM users ORDER BY RANDOM() LIMIT 3").fetchall()
        return followers
    except Exception as ex:
        print(ex)
        return "error"
    finally:
        if "db" in locals():
            db.close()

@get("/app.css")
def _():
    return static_file("app.css", root="./" + web_folder)

@get("/favicon.jpg")
def _():
    return static_file("favicon.jpg", root="./" + web_folder + "images/")

@get("/js/<filename>")
def _(filename):
    return static_file(filename, root="./" + web_folder + "js/")

@get("/avatars/<filename:re:.*\.jpg>")
def _(filename):
    return static_file(filename, root="./" + web_folder + "images/avatars/")

@get("/banners/<filename:re:.*\.jpg>")
def _(filename):
    return static_file(filename, root="./" + web_folder + "images/banners")

@get("/tweets/<filename:re:.*\.jpg>")
def _(filename):
    return static_file(filename, root="./" + web_folder + "images/tweets")

##############################


##############################
# VIEWS
import views.tweet

##############################
# APIS
import apis.api_tweet
import apis.api_sign_up
import apis.api_login

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
