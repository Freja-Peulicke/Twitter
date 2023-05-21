from bottle import post, request, response
import x
import bcrypt

@post("/api-reset-password")
def _():
    try:
        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)
        if logged_in_user:
            response.status = 303
            response.set_header("Location", "/")
            return
        user_password = x.validate_user_password()
        user_password_encoded = user_password.encode()

        x.validate_user_confirm_password()
        salt = bcrypt.gensalt()
        user_id = request.forms.user_id
        user_password_hashed = bcrypt.hashpw(user_password_encoded, salt)

        db = x.db()
        total_rows_updated = db.execute("UPDATE users SET user_password = ? WHERE user_id = ?", (user_password_hashed, user_id,)).rowcount
        if total_rows_updated != 1: raise Exception("Please, try again")
        db.commit()
        print("password updated")
        return {
            "info" : "password updated"
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
        
