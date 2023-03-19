from bottle import post, response
import x
import uuid
import time
import bcrypt
##############################
@post("/api-sign-up")
def _():
    try:
        user_email = x.validate_user_email()
        user_name = x.validate_user_name()
        user_password = x.validate_user_password()
        user_password_encoded = user_password.encode()
        x.validate_user_confirm_password()

        salt = bcrypt.gensalt()

        user_id = str(uuid.uuid4()).replace("-","")
        user = {
            "user_id" : user_id,
            "user_email" : user_email,            
            "user_name" : user_name,
            "user_verification_key" : str(uuid.uuid4()).replace("-",""),
            "user_password": bcrypt.hashpw(user_password_encoded, salt),
            "user_first_name" : "",
            "user_last_name" : "",
            "user_verified_at" : 0,
            "user_created_at" : int(time.time()),
            "user_banner" : "",
            "user_avatar" : "",
            "user_total_tweets" : 0,
            "user_total_followers" : 0,
            "user_total_following" : 0
        }
        # create placed holders for values
        values = ""
        for key in user:
            values += f":{key},"
        values = values.rstrip(",")
        print(values)

        db = x.db()
        total_rows_inserted = db.execute(f"INSERT INTO users VALUES({values})", user).rowcount        
        # total_rows_inserted = db.execute("""
        #     INSERT INTO users VALUES(:user_id, :user_email, :user_name, 
        #     :user_created_at, :user_verification_key, :user_password, :user_first_name, 
        #     :user_last_name, :user_verified_at, :user_banner, :user_avatar, 
        #     :user_total_tweets, :user_total_retweets, :user_total_comments, :user_total_likes, :user_total_dislikes,
        #     :user_total_followers, :user_total_following,)""", user).rowcount
        if total_rows_inserted != 1: raise Exception("Please, try again")
        db.commit()
        return {
            "info" : "user created", 
            "user_id" : user_id
        }
    except Exception as e:
        print(e)
        try: # Controlled exception, usually comming from the x file
            response.status = e.args[0]
            return {"info":e.args[1]}
        except: # Something unknown went wrong
            if "user_email" in str(e): 
                response.status = 400 
                return {"info":"user_email already exists"}
            if "user_name" in str(e): 
                response.status = 400 
                return {"info":"user_name already exists"}
            # unknown scenario
            response.status = 500
            return {"info":str(e)}
    finally:
        if "db" in locals(): db.close()