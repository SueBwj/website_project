from flask_restful import Resource
from services.roleplay_services import RoleplayService
from flask import request
from common.cookies import setUserId

class RoleplayResources(Resource):
    
    @staticmethod
    def get():
        """
        返回roleplay chatbot的对话信息
        """
        user_cookie = request.cookies.get('user_id')
        claim = request.args.get('claim', None)

        if not claim:
            return {'error': 'no claim'}, 400
        if not user_cookie:
            # 第一次进入roleplay
            response = setUserId()
            user_id = response.get_json()['user_id']
            reply = RoleplayService.returnFirstReply(claim, user_id)
            response.set_data(reply)
            return response
        
        