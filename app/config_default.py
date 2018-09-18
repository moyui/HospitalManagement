import os

class Config:
    # 这边进行自定义
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://' #后面自己填写连接数据库

config = {
    'development': DevelopmentConfig
}