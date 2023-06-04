from bottle import post, request, response
import x
import uuid


@post("/api-unlike")
def _():
    try:
        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)
        data = request.json
        like_tweet_fk = "0"
        like_comment_fk = "0"
        if data["type"] == "tweet":
            like_tweet_fk=x.validate_tweet_id(data["tweet_id"].strip())
        elif data["type"] == "comment":
            like_comment_fk=x.validate_comment_id(data["comment_id"].strip())
        else:
            raise Exception("You can only like tweets and comments")
        like_user_fk = logged_in_user['user_id']

        db=x.db()
        cur = db.cursor()
        cur.execute("DELETE FROM likes WHERE like_user_fk = ? AND like_tweet_fk = ? AND like_comment_fk = ?", (like_user_fk, like_tweet_fk, like_comment_fk))
        db.commit()
        return {"info": "ok"}
    except Exception as ex:
        if 'db' in locals(): db.rollback()
        response.status = 400
        return {"info": str(ex)}
    finally:
        if "db" in locals():
            db.close() 