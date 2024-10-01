"""
主要是关于 roleplay 的 api，在聊天框进行对话
"""

from flask_restful import Resource
from services.roleplay_services import RoleplayService, RoleplayPromptService
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

        if not user_cookie or not RoleplayService.file_exist(user_cookie, claim):
            # 第一次进入 roleplay
            response = setUserId()
            reply = RoleplayService.returnFirstReply(claim, user_cookie)
            response.set_data(reply)
            return response

        if not message:
            return {'error': 'message not exist'}, 400

        # 处理常规对话
        reply = RoleplayService.returnReply(user_cookie, claim, message)
        response = make_response({
            "user_id": user_cookie,
        })
        response.set_data(reply)
        return response


class RoleplayPromptResources(Resource):
    
    @staticmethod
    def get():
        """
        根据请求参数返回相应的 roleplay chatbot 回复信息
        """
        claim = request.args.get('claim', None)
        user_cookie = request.cookies.get('user_id')
        if not claim:
            return {'error': 'no claim'}, 400
        
        # 根据 claim 生成 2-3 个问题, 返回一个列表包含三个问题
        question_list = RoleplayPromptService.generate_question(claim,user_cookie)
        return {'question_list': question_list}, 200
    

class CriticalThinkingExerciseResources(Resource):
    """
    提供批判性思维习题训练的资源类.

    该类提供以下功能:
    1. 获取一组批判性思维习题.
    2. 提交用户对习题的答案并获取反馈.
    3. 如果用户回答错误, 使用苏格拉底式提问引导用户找到正确答案.
    """

    def get(self):
        """
        获取一组批判性思维习题.

        第一次请求时, 会生成一组新的习题并存储用户 ID 和习题信息.
        后续请求时, 会返回之前生成的习题.
        """
        user_cookie = request.cookies.get('user_id')

        if not user_cookie or not CriticalThinkingService.exercise_exists(user_cookie):
            # 第一次进入训练
            response = setUserId()
            exercises = CriticalThinkingService.generate_exercises(user_cookie)
            response.set_data({'exercises': exercises})
            return response

        # 返回之前生成的习题
        exercises = CriticalThinkingService.get_exercises(user_cookie)
        return {'exercises': exercises}, 200

    def post(self):
        """
        提交用户对习题的答案并获取反馈.

        如果用户回答错误, 使用苏格拉底式提问引导用户找到正确答案.
        """
        user_cookie = request.cookies.get('user_id')
        if not user_cookie:
            return {'error': 'user_id not found'}, 400

        data = request.get_json()
        exercise_id = data.get('exercise_id')
        answer = data.get('answer')

        if not exercise_id or not answer:
            return {'error': 'missing exercise_id or answer'}, 400

        # 检查答案是否正确
        is_correct, feedback = CriticalThinkingService.check_answer(user_cookie, exercise_id, answer)

        if is_correct:
            return {'feedback': feedback}, 200
        else:
            # 使用苏格拉底式提问引导用户
            guiding_question = CriticalThinkingService.generate_guiding_question(user_cookie, exercise_id)
            return {'feedback': feedback, 'guiding_question': guiding_question}, 200