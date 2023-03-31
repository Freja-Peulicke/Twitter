from bottle import request, response
import sqlite3
import pathlib
import re

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
# Validering af tweet 
TWEET_MIN_LEN = 2
TWEET_MAX_LEN = 5


def validate_tweet():
    error = f"message min {TWEET_MIN_LEN} max {TWEET_MAX_LEN} characters"
    if len(request.forms.message) < TWEET_MIN_LEN:
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


#############################################



#############################################