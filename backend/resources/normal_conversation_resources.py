
from flask_restful import Resource
from flask import make_response, request
from services.normal_conversation_services import NormalConversationService
class NormalConversationResources(Resource):
    
    def get(self):
        """
        根据请求参数返回相应的 normal conversation chatbot 回复信息
        """
        user_cookie = request.cookies.get('user_device_id')
        message = request.args.get('message', None)



        if not message:
            return {'error': 'message not exist'}, 400

        # 处理常规对话
        print(user_cookie, message)
        reply = NormalConversationService.returnReply(str(user_cookie), str(message))
        response = make_response({
            "user_id": user_cookie,
        })
        response.set_data(reply)
        print(response)
        return response