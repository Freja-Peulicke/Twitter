from bottle import post, request, response
import x
import bcrypt
import time
from time import strftime, localtime
##############################
@post("/api-login")
def _():
    try:
        # if user is logged, go to the profile page of that user
        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)
        if logged_in_user: return {"info":"success login", "user_name":logged_in_user["user_name"]}
        # Validate
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        user_password_encoded = user_password.encode()
        # Connect to database
        db = x.db()
        cur = db.cursor()
        user = cur.execute("SELECT * FROM users WHERE user_email = ? LIMIT 1", (user_email,)).fetchone()
        if not user: raise Exception(400, "Invalid credentials. Try again")
        if bcrypt.checkpw(user_password_encoded, user["user_password"]):
            if user["user_blocked_until"] > int(time.time()):
                date = strftime('%Y-%m-%d %H:%M:%S', localtime(user["user_blocked_until"]))
                raise Exception(400, "user blocked until: "+date)
            if user["user_activated_at"] == 0:
                raise Exception(400, "user not activated: check your mail" )
            try:
                import production
                is_cookie_https = True
            except:
                is_cookie_https = False
            response.set_cookie("user", user, secret=x.COOKIE_SECRET, httponly=True, secure=is_cookie_https)
            return {"info":"success login", "user_name":user["user_name"]}
        else:
            raise Exception(400, "Invalid credentials. Try again")
    except Exception as e:
        if 'db' in locals(): db.rollback()
        print(e)
        try: # Controlled exception, usually comming from the x file
            response.status = e.args[0]
            return {"info":e.args[1]}
        except: # Something unknown went wrong
            response.status = 500
            return {"info":str(e)}
    finally:
        if "db" in locals(): db.close()


