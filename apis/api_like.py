from bottle import post, request, response
import x
import uuid
import time


@post("/api-like")
def _():
    try:
        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)
        data = request.json
        tweet_id = "0"
        comment_id = "0"
        if data["type"] == "tweet":
            tweet_id=x.validate_tweet_id(data["tweet_id"].strip())
        elif data["type"] == "comment":
            comment_id=x.validate_comment_id(data["comment_id"].strip())
        else:
            raise Exception("You can only like tweets and comments")
        like_id = str(uuid.uuid4().hex)
        user_id = logged_in_user['user_id']
        like_created_at = int(time.time())
        if not x.validate_like_exist(user_id, tweet_id, comment_id):
            db=x.db()
            total_rows_inserted = db.execute("INSERT INTO likes (like_id, like_user_fk, like_tweet_fk, like_comment_fk, like_created_at) VALUES(?, ?, ?, ?, ?)", (like_id, user_id, tweet_id, comment_id, like_created_at)).rowcount
            if total_rows_inserted != 1: raise Exception("Please, try again")
            db.commit()
            return {"info": "ok"}
        else:
            response.status = 400
            return {"info": "Like already exist"}
    except Exception as ex:
        response.status = 400
        return {"info": str(ex)}
    finally:
        if "db" in locals():
            db.close() 