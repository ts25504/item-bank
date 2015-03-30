class Config:

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development' : DevelopmentConfig,
    'default' : DevelopmentConfig
}

