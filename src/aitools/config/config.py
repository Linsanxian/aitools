import os
from datetime import timedelta

class Config:
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1WCtasOoShKXK82W'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:@localhost/aitools'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'LOmcQxD9S6xUfY57'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # 其他配置
    DEBUG = True 