from bottle import post, request, response
import x
import uuid
import time
import pathlib
import magic

@post("/api-comment")
def _():
    try:  # SUCCESS
        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)
        if not logged_in_user: return {"info":"user not logged in"}

        x.validate_tweet()

        the_image = request.files.get("img-upload")
        if the_image and the_image.filename != "empty":
            image_content = the_image.file.read()
            the_image.file.seek(0)
            mime_type = magic.from_buffer(image_content,mime=True)
            if mime_type not in ("image/png", "image/jpg", "image/jpeg"):
                raise Exception("Please, try again. Image not allowed.")
            ext = pathlib.Path(the_image.filename).suffix
            if ext not in ( ".png", ".jpg", ".jpeg"):
                raise Exception("Please, try again. Image not allowed.")
            image_name = str(uuid.uuid4().hex)
            image_name = image_name + ext
            the_image.save(f"{x.base_dir}images/tweets/{image_name}")
        else:
            image_name = ""
        
        db = x.db()
        tweet_id = request.forms.get("tweet_id")
        comment_id = str(uuid.uuid4().hex)
        comment_message = request.forms.get("message")
        comment_image = image_name
        comment_created_at = int(time.time())
        comment_user_fk = logged_in_user['user_id']
        db.execute("INSERT INTO comments (comment_tweet_fk, comment_id, comment_message, comment_image, comment_created_at, comment_user_fk) VALUES(?, ?, ?, ?, ?, ?)",
                   (tweet_id, comment_id, comment_message, comment_image, comment_created_at, comment_user_fk))
        db.commit()
        return {"info": "ok", "comment_id": comment_id}
    except Exception as ex:  # SOMETHING IS WRONG
        response.status = 400
        return {"info": str(ex)}
    finally:  # This will always take place
        if "db" in locals():
            db.close()
