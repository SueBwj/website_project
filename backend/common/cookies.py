import uuid

from flask import make_response, request


def setUserId():
    user_id = str(uuid.uuid4())
    response = make_response({
      "message":"generate a new user id",
      "user_id":user_id  
    })
    response.set_cookie('user_id',user_id, max_age=30*24*60*60)
    return response


def getUserId():
    """
    获取用户 ID.

    如果请求中包含 user_id Cookie，则返回 Cookie 的值；
    否则，生成新的用户 ID 并返回 None。
    """
    user_cookie = request.cookies.get('user_id')
    if user_cookie:
        return user_cookie
    else:
        return None  # 不在这里设置 Cookie

def generate_uid():
    return str(uuid.uuid4())