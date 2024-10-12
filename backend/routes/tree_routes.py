from flask import Blueprint
from flask_restful import Api
from resources.tree_resources import TreeResources

# 创建蓝图
tree_bp = Blueprint('tree_bp',__name__)
api = Api(tree_bp)

# 定义路由
api.add_resource(TreeResources, '/tree/<int:topic_id>')