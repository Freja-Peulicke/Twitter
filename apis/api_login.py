from bottle import post, request, response
import x
import bcrypt
##############################
@post("/api-login")
def _():
    try:
        # if user is logged, go to the profile page of that user
        user = request.get_cookie("user", secret=x.COOKIE_SECRET)
        if user: return {"info":"success login", "user_name":user["user_name"]}
        # Validate
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        user_password_encoded = user_password.encode()
        # Connect to database
        db = x.db()
        user = db.execute("SELECT * FROM users WHERE user_email = ? LIMIT 1", (user_email,)).fetchone()
        if not user: raise Exception(400, "Cannot login")
        if bcrypt.checkpw(user_password_encoded, user["user_password"]):
            try:
                import production
                is_cookie_https = True
            except:
                is_cookie_https = False
            response.set_cookie("user", user, secret=x.COOKIE_SECRET, httponly=True, secure=is_cookie_https)
            return {"info":"success login", "user_name":user["user_name"]}
        else:
            response.status = 400
            return {"info":"cannot login"}
    except Exception as e:
        print(e)
        try: # Controlled exception, usually comming from the x file
            response.status = e.args[0]
            return {"info":e.args[1]}
        except: # Something unknown went wrong
            response.status = 500
            return {"info":str(e)}
    finally:
        if "db" in locals(): db.close()


