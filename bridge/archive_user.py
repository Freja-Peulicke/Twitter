from bottle import get, request, response
import x



@get("/delete-user/<user_id>")
def _(user_id):
    try:
        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)
        if not logged_in_user:
            response.status = 303
            response.set_header("Location", "/")
            return
        if user_id != logged_in_user["user_id"]:
            response.status = 303
            response.set_header("Location", "/")
            return
        
        db =x.db()
        
        total_rows_deleted = db.execute("DELETE FROM users WHERE user_id = ?", (logged_in_user["user_id"],) ).rowcount
        if total_rows_deleted != 1: raise Exception("Please, try again")
        db.commit()
        
        response.status = 303
        response.set_header("Location", "/logout")
        return
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