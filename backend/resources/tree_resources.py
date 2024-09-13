from flask_restful import Resource
from services.tree_services import TreeServices


class TreeResources(Resource):

    @staticmethod
    def get(topic_id):
        """
        根据topic_id从files文件夹中选取对应的文件，根据tree structure返回到前端
        """
        data = TreeServices.get_tree_structure(topic_id)
        return data, 200
        
