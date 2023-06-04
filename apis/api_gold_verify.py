from bottle import post, request, response
import x
import time

@post("/api-gold-verify")
def _():
    try:
        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)
        data = request.json 
        verify_code =  data["verify_code"]
        if len(verify_code) != 4: raise Exception(400, "Wrong Code")
        db=x.db()
        cur = db.cursor()
        user = cur.execute("SELECT * FROM users WHERE user_id = ? AND user_gold_key = ? LIMIT 1", (logged_in_user["user_id"], verify_code)).fetchone()
        if not user: raise Exception(400, "Wrong code")
        gold_at = int(time.time())
        total_rows_updated = cur.execute("UPDATE users SET user_gold_at = ?, user_gold_key = 0 WHERE user_id = ?", (gold_at, logged_in_user["user_id"])).rowcount
        if total_rows_updated != 1: raise Exception("Please, try again")
        db.commit()
        user = cur.execute("SELECT * FROM users WHERE user_id = ? LIMIT 1", (logged_in_user["user_id"],)).fetchone()
        try:
            import production
            is_cookie_https = True
        except:
            is_cookie_https = False
        response.set_cookie("user", user, secret=x.COOKIE_SECRET, httponly=True, secure=is_cookie_https)
        return {"info": "Gold activated"}
    except Exception as ex:
        if 'db' in locals(): db.rollback()
        return {
            "info": str(ex)
        }
    finally:
        if "db" in locals(): db.close()

