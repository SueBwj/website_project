import uuid

from flask import make_response, request

def setUserId():
    """
    生成新的用户 ID 并设置 Cookie.
    """
    user_id = str(uuid.uuid4())
    response = make_response({
        "message": "generate a new user id",
        "user_id": user_id
    })
    response.set_cookie('user_id', user_id, max_age=30 * 24 * 60 * 60)  # 设置 Cookie 有效期为 30 天
    return user_id

def getUserId():
    """
    获取或设置用户 ID.
    
    如果请求中包含 user_id Cookie，则返回 Cookie 的值；
    否则，生成新的用户 ID 并设置 Cookie，然后返回新的用户 ID.
    """
    user_cookie = request.cookies.get('user_id')
    if user_cookie:
        return user_cookie
    else:
        # 生成新的用户 ID 并设置 Cookie
        user_id = str(uuid.uuid4())
        response = make_response({
            "message": "generate a new user id",
            "user_id": user_id
        })
        response.set_cookie('user_id', user_id, max_age=30 * 24 * 60 * 60)  # 设置 Cookie 有效期为 30 天
        return user_id  # 返回新的用户 ID 和响应对象
def generate_uid():
    """
    生成 UUID.
    
    该函数与 setUserId() 的区别在于，它只生成 UUID，
    而不设置 Cookie.
    """
    return str(uuid.uuid4())