from bottle import post, response, request
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
        user_phone = x.validate_user_phone()
        user_password = x.validate_user_password()
        user_password_encoded = user_password.encode()
        user_first_name = request.forms.user_first_name
        
        x.validate_user_confirm_password()

        salt = bcrypt.gensalt()

        user_id = str(uuid.uuid4()).replace("-","")
        user = {
            "user_id" : user_id,
            "user_email" : user_email,
            "user_phone" : user_phone,            
            "user_name" : user_name,
            "user_gold_key" : "",
            "user_password": bcrypt.hashpw(user_password_encoded, salt),
            "user_first_name" : user_first_name,
            "user_last_name" : "",
            "user_verified_at" : 0,
            "user_created_at" : int(time.time()),
            "user_gold_at" : 0,
            "user_activated_at" : 0,
            "user_banner" : "",
            "user_avatar" : "",
            "user_total_tweets" : 0,
            "user_total_followers" : 0,
            "user_total_following" : 0,
            "user_blocked_until" : 0,
            "user_acrhived_at" : 0
        }
        # create placed holders for values
        values = ""
        for key in user:
            values += f":{key},"
        values = values.rstrip(",")
        print(values)

        db = x.db()
        cur = db.cursor()
        total_rows_inserted = cur.execute(f"INSERT INTO users VALUES({values})", user).rowcount        
        if total_rows_inserted != 1: raise Exception("Please, try again")
        db.commit()
        x.sign_up_email(user_email, user_id)
        return {
            "info" : "user created", 
            "user_id" : user_id
        }
    except Exception as e:
        if 'db' in locals(): db.rollback()
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
            if "user_phone" in str(e): 
                response.status = 400 
                return {"info":"user_phone already exists"}
            # unknown scenario
            response.status = 500
            return {"info":str(e)}
    finally:
        if "db" in locals(): db.close()