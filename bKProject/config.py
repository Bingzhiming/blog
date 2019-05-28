class Config:
    CSRF_ENABLED=True
    SECRET_KEY="www.embsky.com"

    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = "25"
    MAIL_USE_TLS = True
    MAIL_USERNAME = "604363281@qq.com"
    MAIL_PASSWORD = "yxmoxvhuvpnlbdic"

    SQLALCHEMY_TRACK_MODIFICATIONS=True

    @staticmethod
    def init_app(app):
        pass

class DevelopConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/devdb'

class TestConfig(Config):
    TEST = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/testdb'

class ProductConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/embsky'

config = {
    "develop":DevelopConfig,
    "test":TestConfig,
    "product":ProductConfig,
    "default":DevelopConfig
}