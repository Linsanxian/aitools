from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .config.config import Config
from .models import init_app as init_db
from .routes.auth import auth_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化扩展
    CORS(app)
    JWTManager(app)
    init_db(app)
    
    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    return app 