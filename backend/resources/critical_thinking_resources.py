from flask_restful import Resource
from common.cookies import generate_uid, getUserId, setUserId
from services.critical_thinking_services import CriticalThinkingService
from flask import make_response, request

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
        user_cookie = request.args.get('user_device_id')
        claim = request.args.get('claim')

        if not user_cookie or not CriticalThinkingService.exercise_exists(user_cookie):
            # 第一次进入训练
            exercises = CriticalThinkingService.generate_exercises(user_cookie, claim)
            response = make_response({'exercises': exercises})
            response.set_cookie('user_device_id', str(user_cookie))
            return response

        # 返回之前生成的习题
        exercises = CriticalThinkingService.get_exercises(user_cookie)
        response = make_response({'exercises': exercises})
        response.set_cookie('user_device_id', str(user_cookie))
        return response

    def post(self):
        """
        提交用户对习题的答案并获取反馈.

        如果用户回答错误, 使用苏格拉底式提问引导用户找到正确答案.
        """
        user_cookie = getUserId()  # 使用 getUserId() 获取用户 ID
        if not user_cookie:
            return {'error': 'user_device_id not found'}, 400

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