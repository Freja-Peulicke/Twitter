import jwt

the_jwt = jwt.encode({"name":"Freja", "last_name":"Peulicke"}, "the secret", algorithm="HS256")
print(the_jwt)

jwt.decode(the_jwt, "hacking", algorithms="HS256")


#Create the jwt with the users data 
user_jwt = jwt.encode(user, "secret", algorithm="HS256")


