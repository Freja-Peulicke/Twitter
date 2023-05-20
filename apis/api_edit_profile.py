from bottle import post, request, response
import x
import uuid
import pathlib
import magic

@post("/edit-profile")
def _():
    try:
        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)
        user_email = x.validate_user_email()
        user_name = x.validate_user_name()
        user_phone = x.validate_user_phone()
        user_first_name = request.forms.get('user_first_name')
        user_last_name = request.forms.get('user_last_name')

        db = x.db()

        the_banner = request.files.get("banner-upload")
        if the_banner and the_banner.filename != "empty":
            banner_content = the_banner.file.read()
            the_banner.file.seek(0)
            mime_type = magic.from_buffer(banner_content,mime=True)
            if mime_type not in ("image/png", "image/jpg", "image/jpeg"):
                raise Exception("Please, try again. Image not allowed.")
            ext = pathlib.Path(the_banner.filename).suffix
            if ext not in ( ".png", ".jpg", ".jpeg"):
                raise Exception("Please, try again. Image not allowed.")
            banner_name = str(uuid.uuid4().hex)
            banner_name = banner_name + ext
            the_banner.save(f"{x.base_dir}images/banners/{banner_name}")
        else:
            user_data = db.execute("SELECT user_banner FROM users WHERE user_id = ?", (logged_in_user["user_id"],)).fetchone()
            banner_name = user_data["user_banner"]

        the_avatar = request.files.get("avatar-upload")
        if the_avatar and the_avatar.filename != "empty":
            avatar_content = the_avatar.file.read()
            the_avatar.file.seek(0)
            mime_type = magic.from_buffer(avatar_content,mime=True)
            if mime_type not in ("image/png", "image/jpg", "image/jpeg"):
                raise Exception("Please, try again. Image not allowed.")
            ext = pathlib.Path(the_avatar.filename).suffix
            if ext not in ( ".png", ".jpg", ".jpeg"):
                raise Exception("Please, try again. Image not allowed.")
            avatar_name = str(uuid.uuid4().hex)
            avatar_name = avatar_name + ext
            the_avatar.save(f"{x.base_dir}images/avatars/{avatar_name}")
        else:
            user_data = db.execute("SELECT user_avatar FROM users WHERE user_id = ?", (logged_in_user["user_id"],)).fetchone()
            avatar_name = user_data["user_avatar"]
        
        total_rows_updated = db.execute("UPDATE users SET user_first_name = ?, user_last_name = ?, user_name = ?, user_email = ?, user_phone = ?, user_banner = ?, user_avatar = ?  WHERE user_id = ?", (user_first_name, user_last_name, user_name, user_email, user_phone, banner_name, avatar_name, logged_in_user["user_id"],) ).rowcount
        if total_rows_updated != 1: raise Exception("Please, try again")
        db.commit()
        user = db.execute("SELECT * FROM users WHERE user_id = ? LIMIT 1", (logged_in_user["user_id"],)).fetchone()
        try:
            import production
            is_cookie_https = True
        except:
            is_cookie_https = False
        response.set_cookie("user", user, secret=x.COOKIE_SECRET, httponly=True, secure=is_cookie_https)
        return {
            "info" : "user updated"
        }
    except Exception as ex:  # SOMETHING IS WRONG
        response.status = 400
        print(ex)
        return {"info": str(ex)}
    finally: # This will always take place
        if "db" in locals():
            db.close()