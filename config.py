import os

class Config:
    SECRET_KEY = 'juru1'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://wecode:  @localhost/pitch'
   
    @staticmethod
    def init_app(app):
        pass


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig

}