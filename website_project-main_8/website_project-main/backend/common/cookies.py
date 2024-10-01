import uuid

from flask import make_response


def setUserId():
    user_id = str(uuid.uuid4())
    response = make_response({
      "message":"generate a new user id",
      "user_id":user_id  
    })
    response.set_cookie('user_id',user_id, max_age=30*24*60*60)
    return response

def generate_uid():
    return str(uuid.uuid4())