from flask_restful import Resource
from services.roleplay_services import RoleplayService

class RoleplayResources(Resource):
    
    @staticmethod
    def get(claim):
        """
        返回roleplay chatbot的对话信息
        """
        
        