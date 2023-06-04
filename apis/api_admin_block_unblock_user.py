from bottle import post, request, response
import time
import x

@post("/api-admin-block-unblock-user")
def _():
    try:
        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)
        if not logged_in_user or logged_in_user["user_admin"] == 0:
            response.status = 303
            response.set_header("Location", "/")
            return
        
        db = x.db()
        cur = db.cursor()

        data = request.json

        user_id = x.validate_user_id(data["user_id"])

        user = cur.execute("SELECT * FROM users WHERE user_id = ? LIMIT 1", (user_id,)).fetchone()
        
        if user["user_blocked_until"] > int(time.time()):
            # Unblock
            print("Unblock")
            total_rows_updated = cur.execute("UPDATE users SET user_blocked_until = 0 WHERE user_id = ?", (user["user_id"],)).rowcount
            if total_rows_updated != 1: raise Exception("Please, try again. User not unblocked!")
            db.commit()
            x.admin_unblock_user_email(user["user_email"])
            return {"info": "User unblocked and email sent"}
        else:
            # Block
            print("Block")
            user_blocked_until = int(time.time() + (24 * 60 * 60))   # Current time and add 24 hours (24 hours * 60 minutes * 60 seconds)
            total_rows_updated = cur.execute("UPDATE users SET user_blocked_until = ? WHERE user_id = ? AND user_admin = 0", (user_blocked_until, user["user_id"],)).rowcount
            if total_rows_updated != 1: raise Exception("Please, try again. User not blocked!")
            db.commit()
            x.admin_block_user_email(user["user_email"])
            return {"info": "User blocked and email sent"}
    
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