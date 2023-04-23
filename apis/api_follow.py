from bottle import post, request, response
import x
import time


@post("/api-follow")
def _():
    try:
        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)
        data = request.json
        followee_id = x.validate_user_id(data["followee"])
        follower_id = logged_in_user['user_id']
        followed_at = int(time.time())
        if not x.validate_follow_exist(follower_id,followee_id):
            db =x.db()
            db.execute(
                "INSERT INTO followers (follower_fk, followee_fk, followed_at) VALUES (?,?,?)",(follower_id, followee_id, followed_at))
            db.commit()
            return {"info": "ok"}
        else:
            response.status = 400
            return {"info": "Follow already exist"}
    except Exception as ex:
        response.status = 400
        return {"info": str(ex)}
    finally:
        if "db" in locals():
            db.close()