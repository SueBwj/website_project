from flask import Blueprint
from flask_restful import Api
from resources.normal_conversation_resources import NormalConversationResources

# 创建蓝图
normal_conversation_bp = Blueprint('normal_conversation_bp',__name__)
api = Api(normal_conversation_bp)

# 定义路由
api.add_resource(NormalConversationResources, '/normal_conversation')