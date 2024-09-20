from flask_restful import Resource
from services.roleplay_services import RoleplayService
from flask import make_response, request
from common.cookies import setUserId

class RoleplayResources(Resource):
    
    def get(self):
        """
        根据请求参数返回相应的 roleplay chatbot 回复信息
        """
        user_cookie = request.cookies.get('user_id')
        claim = request.args.get('claim', None)
        message = request.args.get('message', None)

        if not claim:
            return {'error': 'no claim'}, 400

        if not user_cookie:
            # 第一次进入 roleplay
            response = setUserId()
            user_id = response.get_json().get('user_id')
            if not user_id:
                return {'error': 'failed to set user_id'}, 500
            reply = RoleplayService.returnFirstReply(claim, user_id)
            response.set_data(reply)
            return response

        if not message:
            return {'error': 'message not exist'}, 400

        # 处理常规对话
        reply = RoleplayService.returnReply(user_cookie, claim, message)
        return make_response({
            "reply": reply 
        })

