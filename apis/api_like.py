from bottle import post, request, response
import x
import uuid
import time


@post("/api-like")
def _():
    try:
        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)

        like_tweet_fk = "0"
        like_comment_fk = "0"
        if request.forms.type=="tweet":
            like_tweet_fk=x.validate_tweet_id()
        elif request.forms.type=="comment":
            like_comment_fk=x.validate_comment_id()
        else:
            raise Exception("You can only like tweets and comments")
        like_id = str(uuid.uuid4().hex)
        like_user_fk = logged_in_user['user_id']
        like_created_at = int(time.time())
        db=x.db()
        total_rows_inserted = db.execute("INSERT INTO likes (like_id, like_user_fk, like_tweet_fk, like_comment_fk, like_created_at) VALUES(?, ?, ?, ?, ?)", (like_id, like_user_fk, like_tweet_fk, like_comment_fk, like_created_at)).rowcount
        if total_rows_inserted != 1: raise Exception("Please, try again")
        db.commit()
        return "Succes"
    except Exception as ex:
        response.status = 400
        return {"info": str(ex)}
    finally:
        if "db" in locals():
            db.close() 