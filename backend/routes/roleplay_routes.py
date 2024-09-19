from flask import Blueprint
from flask_restful import Api
from resources.roleplay_resoources import RoleplayResources

# 创建蓝图
roleplay_bp = Blueprint('roleplay_bp',__name__)
api = Api(roleplay_bp)

# 定义路由
api.add_resource(RoleplayResources, '/roleplay')