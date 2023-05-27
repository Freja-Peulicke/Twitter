from bottle import post, request, response
import x

@post("/api-archive-user")
def _():
    try:
        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)
        if not logged_in_user:
            response.status = 303
            response.set_header("Location", "/")
            return

        x.delete_user_email(logged_in_user["user_email"],logged_in_user["user_id"])
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
        

