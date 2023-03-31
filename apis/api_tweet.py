from bottle import post, request, response
import x
import uuid
import time


@post("/tweet")
def _():
    try:  # SUCCESS
        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)

        x.validate_tweet()
        db = x.db()
        # tweet_id = str(uuid.uuid4()).replace("-","")
        tweet_id = str(uuid.uuid4().hex)
        tweet_message = request.forms.get("message")
        tweet_image = ""
        tweet_created_at = int(time.time())
        tweet_user_fk = logged_in_user['user_id']
        db.execute("INSERT INTO tweets (tweet_id, tweet_message, tweet_image, tweet_created_at, tweet_user_fk) VALUES(?, ?, ?, ?, ?)",
                   (tweet_id, tweet_message, tweet_image, tweet_created_at, tweet_user_fk))
        db.commit()
        return {"info": "ok", "tweet_id": tweet_id}
    except Exception as ex:  # SOMETHING IS WRONG
        response.status = 400
        return {"info": str(ex)}
    finally:  # This will always take place
        if "db" in locals():
            db.close()
