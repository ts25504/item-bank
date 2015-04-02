import os

class Config:
    SECRET_KEY = 'hard to guess string'
    MYSQL_USERNAME = os.environ.get('MYSQL_USERNAME')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_HOSTNAME = os.environ.get('MYSQL_HOSTNAME')
    MYSQL_DEV_DB = os.environ.get('MYSQL_DEV_DB')
    MYSQL_PRODUCT_DB = os.environ.get('MYSQL_PRODUCT_DB')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s/%s' % (Config.MYSQL_USERNAME,
            Config.MYSQL_PASSWORD, Config.MYSQL_HOSTNAME, Config.MYSQL_DEV_DB)
    DEBUG = True

config = {
        'development' : DevelopmentConfig,
        'default' : DevelopmentConfig
        }
