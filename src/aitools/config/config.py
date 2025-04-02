import os
from datetime import timedelta


class Config:
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1WCtasOoShKXK82W'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'mysql+pymysql://root:@localhost/aitools'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'LOmcQxD9S6xUfY57'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    # 其他配置
    DEBUG = True

    # DashScope API 密钥
    DASHSCOPE_API_KEY = os.environ.get(
        'DASHSCOPE_API_KEY') or 'sk-7c7ba0b42fce4e26b2b6570ffa919cc2'
    DASHSCOPE_BASE_URL = os.environ.get(
        'DASHSCOPE_BASE_URL') or 'https://dashscope.aliyuncs.com/compatible-mode/v1'
