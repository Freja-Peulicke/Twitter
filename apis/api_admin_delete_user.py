from bottle import post, request, response
import x

@post("/api-admin-delete-user")
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

        cur.execute("PRAGMA foreign_keys = 0")

        total_rows_deleted = cur.execute("DELETE FROM users WHERE user_id = ? AND user_admin = 0", (user["user_id"],) ).rowcount
        if total_rows_deleted != 1: raise Exception("Please, try again")
        db.commit()

        cur.execute("PRAGMA foreign_keys = 1")

        x.admin_delete_user_email(user["user_email"])

        return {
            "info" : "user deleted and email sent"
        }
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