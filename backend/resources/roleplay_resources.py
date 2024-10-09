"""
主要是关于 roleplay 的 api，在聊天框进行对话
"""

import json
from flask_restful import Resource
from services.roleplay_services import RoleplayService, RoleplayPromptService
from flask import make_response, request
from common.cookies import generate_uid, setUserId

class RoleplayResources(Resource):
    
    def get(self):
        """
        根据请求参数返回相应的 roleplay chatbot 回复信息
        """
        user_cookie = request.cookies.get('user_device_id')
        print(user_cookie)
        claim = request.args.get('claim', None)
        message = request.args.get('message', None)
        topic_id = request.args.get('topic_id', None)

        if not claim:
            return {'error': 'no claim'}, 400

        if not RoleplayService.file_exist(user_cookie, claim):
            # 第一次进入 roleplay
            reply, all_comments = RoleplayService.returnFirstReply(claim, user_cookie,topic_id)
            response = make_response({
                "user_id": user_cookie,
            })
            data = {'reply': reply, 'all_comments': all_comments}
            response.set_data(json.dumps(data).encode('utf-8'))
            return response

        if not message:
            return {'error': 'message not exist'}, 400

        # 处理常规对话
        print(user_cookie, claim, message)
        reply = RoleplayService.returnReply(user_cookie, claim, message)
        response = make_response({
            "user_id": user_cookie,
        })
        data = {'reply': reply, 'all_comments': ''}
        response.set_data(json.dumps(data).encode('utf-8'))
        print(response)
        return response


class RoleplayPromptResources(Resource):
    
    @staticmethod
    def get():
        """
        根据请求参数返回相应的 roleplay chatbot 回复信息
        """
        claim = request.args.get('claim', None)
        topic_id = request.args.get('topic_id', None)

        user_cookie = request.cookies.get('user_id')
        if not claim:
            return {'error': 'no claim'}, 400
        
        # 根据 claim 生成 2-3 个问题, 返回一个列表包含三个问题
        question_list = RoleplayPromptService.generate_question(claim,user_cookie, topic_id)
        return {'question_list': question_list}, 200