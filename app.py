from bottle import default_app, get, post, request, response, run, static_file, template
import x



# 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
# https://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@github.com/frej1187/twitter.git
#########################
#########################

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
    repo.create_head('main', origin.refs.main).set_tracking_branch(
        origin.refs.main).checkout()
    origin.pull()
    return ""


##################################################
# flyttes til views/index.py
@get("/")
def render_index():
    try:
        response.add_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        response.add_header("Pragma", "no-cache")
        response.add_header("Expires", 0)

        logged_in_user = request.get_cookie("user", secret="my-secret")

        db = x.db()
        suggested_followers = get_suggested_followers()
        tweets = db.execute(
            "SELECT users.id AS user_id, message, image, tweets.created_at AS tweet_created_at, replies, retweets, likes, views, username, first_name, last_name FROM tweets JOIN users ON user_fk = users.id ORDER BY RANDOM() LIMIT 5").fetchall()
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
        response.add_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        response.add_header("Pragma", "no-cache")
        response.add_header("Expires", 0)
 
        logged_in_user = request.get_cookie("user", secret="my-secret")
        suggested_followers = get_suggested_followers()
        db = x.db()
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

# funktion der gør at vi kan bruge keys fra databasen når vi skal kigge i data'en
# Så vi kan bruge user["user_id"], user["user_name"], user["user_email"] etc. i stedet for user[0], user[1], user[2] etc,
def dict_factory(cursor, row):
    col_names = [col[0] for col in cursor.description]
    return {key: value for key, value in zip(col_names, row)}

# Henter 3 rækker fra vores users table i databasen, som vi bruger til suggested followers
def get_suggested_followers():
    try:
        db = x.db()
        followers = db.execute(
            "SELECT * FROM users LIMIT 3").fetchall()
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
# BRIDGE 
# Slettes når rigtigt login er lavet
import bro.login

##############################
# VIEWS
import views.tweet

##############################
# APIS
import apis.api_tweet
#import apis.api_sign_up

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
