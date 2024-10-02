from flask import Blueprint
from flask_restful import Api
from resources.critical_thinking_resources import CriticalThinkingExerciseResources

# 创建蓝图
critical_thinking_bp = Blueprint('critical_thinking_bp',__name__)
api = Api(critical_thinking_bp)


api.add_resource(CriticalThinkingExerciseResources, '/critical_thinking')