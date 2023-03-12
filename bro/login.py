from bottle import post, response
import time

@post("/login")
def _():
    #Redirection
    #status code
    #the redirected page

    #response.status= 300
    #response.set_header("Location", "/login")
    logged_in_user = {
        "user_name":"Peulicke",
        "user_first_name":"Freja",
        "user_last_name": "Peulice"
    }
    cookie_expiration_date = int (time.time()) + 7200
    response.set_cookie("user", logged_in_user, secret="my-secret", httponly=True)
    response.status = 303
    response.set_header("Location", "/")
    return