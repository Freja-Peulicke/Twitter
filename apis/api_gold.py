from bottle import get, post, response, request
import x
import random
import requests
import json


@post("/api-gold")
def _():
    try:
        logged_in_user = request.get_cookie("user", secret=x.COOKIE_SECRET)
        randomNumber = random.randrange(0,2000)
        randomNumberStr = str(randomNumber)
        if len(randomNumberStr)== 1:
            randomNumberStr = "000" + randomNumberStr
        elif len(randomNumberStr)==2:
            randomNumberStr = "00" + randomNumberStr
        elif len(randomNumberStr)==3:
            randomNumberStr = "0" + randomNumberStr
        db=x.db()
        total_rows_updated = db.execute("UPDATE users SET user_gold_key = ? WHERE user_id = ?", (randomNumberStr, logged_in_user["user_id"], )).rowcount
        if total_rows_updated != 1: raise Exception("Please, try again")
        db.commit()
        user_api_key = "394cf1eb0df808b48563d7cd5623fc10"
        sms_message = "Your code is " + randomNumberStr
        sms_to_phone = logged_in_user["user_phone"]

        payload = {	"user_api_key":user_api_key, 
                    "sms_message":sms_message, 
                    "sms_to_phone":sms_to_phone}

        res = requests.post('https://fiotext.com/send-sms', data=payload)
        return res.text
    except Exception as ex:
        return {
            "info": str(ex)
        }
    finally:
        if "db" in locals(): db.close()









