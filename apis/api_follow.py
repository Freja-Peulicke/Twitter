from bottle import post, request, response
import x
import time


@post("/api-follow")
def _():
    try:
        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)
        data = request.json
        followee_id = data["followee"]
        follower_id = logged_in_user['user_id']
        followed_at = int(time.time())
        
        db =x.db()
        db.execute(
            "INSERT INTO followers (follower_fk, followee_fk, followed_at) VALUES (?,?,?)",(follower_id, followee_id, followed_at))
        db.commit()
        return {"info": "ok"}
    except Exception as ex:
        response.status = 400
        return {"info": str(ex)}
    finally:
        if "db" in locals():
            db.close()