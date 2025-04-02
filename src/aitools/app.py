from flask import Flask
from flask_cors import CORS
from .routes.food import food_bp

def create_app():
    app = Flask(__name__)
    
    # 配置 CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["*"],  # 允许的前端域名
            "methods": ["*"],  # 允许的 HTTP 方法
            "allow_headers": ["*"],      # 允许的请求头
            "supports_credentials": True            # 允许携带认证信息
        }
    })

    # 注册蓝图，指定 URL 前缀
    app.register_blueprint(food_bp)

    return app 