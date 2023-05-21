from bottle import post, request, response
import x

@post("/api-forgot-password")
def _():
    try:
        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)
        if logged_in_user:
            response.status = 303
            response.set_header("Location", "/")
            return

        user_email = x.validate_user_email()
        db = x.db()
        user = db.execute("SELECT * FROM users WHERE user_email = ? LIMIT 1", (user_email,)).fetchone()
        if not user: raise Exception(400, "Try again")
        x.forgot_password_email(user_email, user["user_id"])
        return {
            "info" : "email sent"
        }
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
        
