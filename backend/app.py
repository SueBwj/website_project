from flask import Flask
from flask_cors import CORS
from routes.tree_routes import tree_bp

app = Flask(__name__)
CORS(app)
# 注册蓝图
app.register_blueprint(tree_bp)

if __name__ == '__main__':
    app.run(debug=True)