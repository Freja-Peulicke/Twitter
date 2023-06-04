from bottle import post, request, response
import x
import uuid
import time

@post("/api-retweet")
def _():
    try:  # SUCCESS
        print("retweet start")
        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)

        db = x.db()
        cur = db.cursor()
        tweet_id = str(uuid.uuid4().hex)
        tweet_retweet_fk = request.json["tweet_id"]
        tweet_created_at = int(time.time())
        tweet_user_fk = logged_in_user['user_id']
        cur.execute("INSERT INTO tweets (tweet_id, tweet_retweet_fk, tweet_created_at, tweet_user_fk) VALUES(?, ?, ?, ?)",
                   (tweet_id, tweet_retweet_fk, tweet_created_at, tweet_user_fk))
        db.commit()

        print("retweet end")
        return {"info": "ok", "tweet_id": tweet_id}
    except Exception as ex:  # SOMETHING IS WRONG
        if 'db' in locals(): db.rollback()
        response.status = 400
        return {"info": str(ex)}
    finally:  # This will always take place
        if "db" in locals():
            db.close()
