from bottle import post, request, response
import x
import uuid
import time
import pathlib
from pathlib import Path
import magic


@post("/tweet")
def _():
    try:  # SUCCESS
        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)

        x.validate_tweet()

        the_image = request.files.get("img-upload")
        if the_image is not None:
            print("### 1")
            image_content = the_image.file.read()
            print("### 2")
            the_image.file.seek(0)
            print("### 3")
            mime_type = magic.from_buffer(image_content,mime=True)
            print("### 4")
            if mime_type not in ("image/png", "image/jpg", "image/jpeg"):
                print("### 4a")
                raise Exception("Please, try again. Image not allowed.")
            # name, ext = os.path.splitext(the_image.filename)
            print("### 5")
            ext = pathlib.Path(the_image.filename).suffix
            print("### 6")
            if ext not in ( ".png", ".jpg", ".jpeg"):
                print("### 6a")
                raise Exception("Please, try again. Image not allowed.")
            print("### 7")
            image_name = str(uuid.uuid4().hex)
            print("### 8")
            image_name = image_name + ext
            print("### 9")
            #print(f"{x.base_dir}images/tweets/{image_name}")
            the_image.save(f"{x.base_dir}images/tweets/{image_name}")
            #the_image.save(f"images/tweets/{image_name}")
            print("### 10")
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
        print("### Error")
        response.status = 400
        return {"info": str(ex)}
    finally:  # This will always take place
        if "db" in locals():
            db.close()
