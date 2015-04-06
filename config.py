import os

class Config:
    SECRET_KEY = 'hard to guess string'
    MYSQL_USERNAME = os.environ.get('MYSQL_USERNAME')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_HOSTNAME = os.environ.get('MYSQL_HOSTNAME')
    MYSQL_DEV_DB = os.environ.get('MYSQL_DEV_DB')
    MYSQL_TEST_DB = os.environ.get('MYSQL_TEST_DB')
    MYSQL_PRODUCT_DB = os.environ.get('MYSQL_PRODUCT_DB')
    QUESTIONS_PER_PAGE = 15
    ALLOWED_TAGS = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                    'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                    'h1', 'h2', 'h3', 'p', 'img', 'br', 'sub', 'sup']
    ALLOWED_ATTRIBUTES = {
            '*' : ['class'],
            'a' : ['href'],
            'img' : ['src', 'alt'],
            }

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s/%s' % (Config.MYSQL_USERNAME,
            Config.MYSQL_PASSWORD, Config.MYSQL_HOSTNAME, Config.MYSQL_DEV_DB)
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s/%s' % (Config.MYSQL_USERNAME,
            Config.MYSQL_PASSWORD, Config.MYSQL_HOSTNAME, Config.MYSQL_TEST_DB)

config = {
        'development' : DevelopmentConfig,
        'testing' : TestingConfig,
        'default' : DevelopmentConfig
        }
