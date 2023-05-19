from bottle import post, request, response
import x
import uuid
import time
import pathlib
import magic


@post("/tweet")
def _():
    try:  # SUCCESS
        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)

        x.validate_tweet()

        the_image = request.files.get("img-upload")
        if the_image is not None:
            image_content = the_image.file.read()
            the_image.file.seek(0)
            mime_type = magic.from_buffer(image_content,mime=True)
            if mime_type not in ("image/png", "image/jpg", "image/jpeg"):
                raise Exception("Please, try again. Image not allowed.")
            # name, ext = os.path.splitext(the_image.filename)
            ext = pathlib.Path(the_image.filename).suffix
            if ext not in ( ".png", ".jpg", ".jpeg"):
                raise Exception("Please, try again. Image not allowed.")
            image_name = str(uuid.uuid4().hex)
            image_name = image_name + ext 
            the_image.save(f"images/tweets/{image_name}")
        else:
            image_name = ""
        
        db = x.db()
        
        tweet_id = str(uuid.uuid4().hex)
        tweet_message = request.forms.get("message")
        tweet_image = image_name
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
