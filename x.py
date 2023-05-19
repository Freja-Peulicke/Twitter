from bottle import request, response
import sqlite3
import pathlib
import re
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

COOKIE_SECRET = "41ebeca46feb-4d77-a8e2-554659074C6319a2fbfb-9a2D-4fb6-Afcad32abb26a5e0"

#############################

# funktion der gør at vi kan bruge keys fra databasen når vi skal kigge i data'en
# Så vi kan bruge user["user_id"], user["user_name"], user["user_email"] etc. i stedet for user[0], user[1], user[2] etc,
def dict_factory(cursor, row):
    col_names = [col[0] for col in cursor.description]
    return {key: value for key, value in zip(col_names, row)}

##############################
#funktion der opretter forbindelse til databasen

def db():
    try:
        db = sqlite3.connect(str(pathlib.Path(__file__).parent.resolve())+"/twitter.db")
        db.execute("PRAGMA foreign_keys=ON")
        db.row_factory = dict_factory
        return db
    except Exception as ex:
        print(ex)
    finally:
        pass

##############################

### for at undgå at uploade de statiske filer, er ikke noget santiago har. 
try:
    import production
    domain = "https://fpj.eu.pythonanywhere.com"
# Run in local computer
except Exception as ex:
    domain = "http://127.0.0.1:3001"

def sign_up_email(receiver_email, user_id):
    try:
        sender_email = "freja.peulicke@gmail.com"
        password = "pliyoscaqcaahfjq"   
        message = MIMEMultipart("alternative")
        message["Subject"] = "multipart test"
        message["From"] = sender_email
        message["To"] = receiver_email 
        # Create the plain-text and HTML version of your message
        text = f"""\
        Hi,
        Thank you for signing up, we are glad you are here!
        Click here to activate: {domain}/activate/{user_id}"""
        html = f"""\
        <html>
        <body>
            <p>Hi,<br>
            Thank you for signing up, we are glad you are here!<br>
            <a href="{domain}/activate/{user_id}">Click here to activate</a>
            </p>
        </body>
        </html>
        """   
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )   
    except:
        pass
    finally:
        pass




##############################
# Validering af tweet 
TWEET_MIN_LEN = 2
TWEET_MAX_LEN = 180


def validate_tweet():
    error = f"message min {TWEET_MIN_LEN} max {TWEET_MAX_LEN} characters"
    the_image = request.files.get("img-upload")
    if len(request.forms.message) < TWEET_MIN_LEN and the_image is None:
        raise Exception(400, error)
    if len(request.forms.message) > TWEET_MAX_LEN:
        raise Exception(400, error)
    return request.forms.get("message")
####################################


## regex er langsom derfor tjekker vi selv for min og max

USER_NAME_MIN = 4
USER_NAME_MAX = 15
USER_NAME_REGEX = "^[a-zA-Z0-9_]*$"

def validate_user_name():
    print("*"*30)
    print(request.forms.user_name)
    error = f"user_name {USER_NAME_MIN} to {USER_NAME_MAX} english letters or number from 0 to 9 and _"
    request.forms.user_name = request.forms.user_name.strip()
    if len(request.forms.user_name) < USER_NAME_MIN: raise Exception(400, error)
    if len(request.forms.user_name) > USER_NAME_MAX: raise Exception(400, error)
    if not re.match(USER_NAME_REGEX, request.forms.user_name): raise Exception(400, error)
    return request.forms.user_name


USER_PHONE_MIN = 8
USER_PHONE_MAX = 8
USER_PHONE_REGEX = "^[0-9]*$"

def validate_user_phone():
    print("*"*30)
    print(request.forms.user_phone)
    error = f"user_phone {USER_PHONE_MIN} to {USER_PHONE_MAX} number from 0 to 9"
    request.forms.user_phone = request.forms.user_phone.strip()
    if len(request.forms.user_phone) < USER_PHONE_MIN: raise Exception(400, error)
    if len(request.forms.user_phone) > USER_PHONE_MAX: raise Exception(400, error)
    if not re.match(USER_PHONE_REGEX, request.forms.user_phone): raise Exception(400, error)
    return request.forms.user_phone
#############################################
# Funktion der deaktivere cache
def disable_cache():
    response.add_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0")
    response.add_header("Pragma", "no-cache")
    response.add_header("Expires", 0) 

#############################################
# 
def validate_user_logged():
    user = request.get_cookie("user", secret=COOKIE_SECRET)
    if user is None: raise Exception(400, "user must login")
    return user


#############################################
#Validere email-adresse 

USER_EMAIL_MIN = 6
USER_EMAIL_MAX = 100
USER_EMAIL_REGEX = "^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"

def validate_user_email():
	error = f"user_email invalid"
	request.forms.user_email = request.forms.user_email.strip()
	if len(request.forms.user_email) < USER_EMAIL_MIN : raise Exception(400, error)
	if len(request.forms.user_email) > USER_EMAIL_MAX : raise Exception(400, error)  
	if not re.match(USER_EMAIL_REGEX, request.forms.user_email): raise Exception(400, error)
	return request.forms.user_email

#############################################
USER_PASSWORD_MIN = 6
USER_PASSWORD_MAX = 50

def validate_user_password():
	error = f"user_password {USER_PASSWORD_MIN} to {USER_PASSWORD_MAX} characters"
	request.forms.user_password = request.forms.user_password.strip()
	if len(request.forms.user_password) < USER_PASSWORD_MIN : raise Exception(400, error)
	if len(request.forms.user_password) > USER_PASSWORD_MAX : raise Exception(400, error)
	return request.forms.user_password

def validate_user_confirm_password():
	error = f"user_password and user_confirm_password do not match"
	request.forms.user_password = request.forms.user_password.strip()
	request.forms.user_confirm_password = request.forms.user_confirm_password.strip()
	if request.forms.user_confirm_password != request.forms.user_password: raise Exception(400, error)
	return request.forms.user_confirm_password

#############################################
def validate_tweet_id(tweet_id):
    try:
        db_tweet_validate=db()
        tweet = db_tweet_validate.execute("SELECT * FROM tweets WHERE tweet_id = ? LIMIT 1", (tweet_id,)).fetchone()
        if not tweet: raise Exception(400, "Cannot like non existing tweet")
        return tweet_id
    except Exception as ex:
        response.status = 400
        return {"info": str(ex)}
    finally:
        if "db_tweet_validate" in locals():
            db_tweet_validate.close()

#############################################
def validate_comment_id(comment_id):
    try:
        db_comment_validate=db()
        comment = db_comment_validate.execute("SELECT * FROM comments WHERE comment_id = ? LIMIT 1", (comment_id,)).fetchone()
        if not comment: raise Exception(400, "Cannot like non existing comment")
        return comment_id
    except Exception as ex:
        response.status = 400
        return {"info": str(ex)}
    finally:
        if "db_comment_validate" in locals():
            db_comment_validate.close()


#############################################

def validate_user_id(user_id):
    try:
        db_user_validate=db()
        user = db_user_validate.execute("SELECT * FROM users WHERE user_id = ? LIMIT 1", (user_id,)).fetchone()
        if not user: raise Exception(400, "User does not exist")
        return user_id
    except Exception as ex:
        response.status = 400
        return {"info": str(ex)}
    finally:
        if "db_user_validate" in locals():
            db_user_validate.close()

#############################################

def validate_follow_exist(follower_id, followee_id):
    try:
        db_follow_validate=db()
        follow = db_follow_validate.execute("SELECT * FROM followers WHERE follower_fk = ? AND followee_fk = ? LIMIT 1", (follower_id, followee_id ,)).fetchone()
        if follow: raise Exception(400, "Follow already exist")
        return False
    except Exception as ex:
        return True
    finally:
        if "db_follow_validate" in locals():
            db_follow_validate.close()

#############################################

def validate_like_exist(user_id, tweet_id, comment_id):
    try:
        db_like_validate=db()
        like = db_like_validate.execute("SELECT * FROM likes WHERE like_user_fk = ? AND like_tweet_fk = ? AND like_comment_fk = ? LIMIT 1", (user_id, tweet_id, comment_id ,)).fetchone()
        if like: raise Exception(400, "Like already exist")
        return False
    except Exception as ex:
        return True
    finally:
        if "db_like_validate" in locals():
            db_like_validate.close()
