from bottle import post, request, response
import x
import time


@post("/api-unfollow")
def _():
    try:
        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)
        data = request.json
        followee_id = data["followee"]
        follower_id = logged_in_user['user_id']
        
        db =x.db()
        cur = db.cursor()
        cur.execute(
            "DELETE FROM followers WHERE follower_fk = ? AND followee_fk = ?",(follower_id, followee_id))
        db.commit()
        return {"info": "ok"}
    except Exception as ex:
        if 'db' in locals(): db.rollback()
        response.status = 400
        return {"info": str(ex)}
    finally:
        if "db" in locals():
            db.close()