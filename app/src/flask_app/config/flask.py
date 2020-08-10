class DevelopmentConfig:
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{pswd}@{host}:{port}/{db_name}?charset=utf8'.format(
        user='root',
        pswd='password',
        host='mysql',
        port='3306',
        db_name='develop'
    )
    SECRET_KEY = b'\xf0\x03E)\xd7\xc3\x8f\x85\x89\x8b\xb4\x08V\xe2*\xd8'
