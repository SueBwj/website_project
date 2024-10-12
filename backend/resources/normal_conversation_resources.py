
from flask_restful import Resource
from flask import make_response, request
from services.normal_conversation_services import NormalConversationService
from common.cookies import generate_uid

class NormalConversationResources(Resource):
    
    def get(self):
        """
        根据请求参数返回相应的 normal conversation chatbot 回复信息
        """
        user_cookie = request.cookies.get('user_id')
        if not user_cookie:
            user_cookie = generate_uid()

        message = request.args.get('message', None)
        topic = request.args.get('topic', None)


        if not message:
            return {'error': 'message not exist'}, 400

        # 处理常规对话
        print(user_cookie, message)
        reply = NormalConversationService.returnReply(str(user_cookie), str(message), str(topic))
        response = make_response()
        response.set_data(reply)
        response.set_cookie('user_id', user_cookie)
        print(response)
        return response