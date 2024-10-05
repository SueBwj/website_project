from flask import Flask
from flask_cors import CORS
from services.roleplay_services import RoleplayService
from routes.tree_routes import tree_bp
from routes.roleplay_routes import roleplay_bp
from routes.critical_thinking_routes import critical_thinking_bp
from routes.normal_conversation_routes import normal_conversation_bp

app = Flask(__name__)
CORS(app, supports_credentials=True)
# 注册蓝图
app.register_blueprint(tree_bp)
app.register_blueprint(roleplay_bp)
app.register_blueprint(critical_thinking_bp)
app.register_blueprint(normal_conversation_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)