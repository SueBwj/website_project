from flask import Flask
from flask_cors import CORS
from services.roleplay_services import RoleplayService
from routes.tree_routes import tree_bp
from routes.roleplay_routes import roleplay_bp

app = Flask(__name__)
CORS(app)
# 注册蓝图
app.register_blueprint(tree_bp)
app.register_blueprint(roleplay_bp)


if __name__ == '__main__':
    app.run(debug=True, port=5000)