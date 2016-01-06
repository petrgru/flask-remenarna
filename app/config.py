import os
from sqlalchemy.engine.url import URL

class base_config(object):
    """Default configuration options."""
    SITE_NAME = 'remenarna-xml'
#    SERVER_NAME = 'ms.sspu-opava.cz:8081'
    SERVER_NAME = 'localhost:5000'
    SECRET_KEY = '1234567823333'

    MAIL_SERVER = '192.168.22.4'
    MAIL_PORT = '25'

    REDIS_HOST = 'localhost'
    REDIS_PORT = '6379'

    BROKER_URL = 'redis://{}:{}'.format(REDIS_HOST, REDIS_PORT)
    BROKER_BACKEND = BROKER_URL

    CACHE_HOST = 'localhost'
    CACHE_PORT = '11211'
    APP_DIR = os.path.dirname(os.path.abspath(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    DB_NAME = 'dev.db'
    DB_PATH = os.path.join(PROJECT_ROOT, DB_NAME)
#    DB_PATH = os.path.join('/media/ramdisk/', DB_NAME)
    SQLALCHEMY_DATABASE_URI = URL(drivername='sqlite', database=DB_PATH)

    SUPPORTED_LOCALES = ['en']


class dev_config(base_config):
    """Development configuration options."""
    DEBUG = True
    ASSETS_DEBUG = True
    WTF_CSRF_ENABLED = False
    ENV = 'dev'

    DEBUG = True

    DB_NAME = 'dev.db'
    DB_PATH = os.path.join(base_config.PROJECT_ROOT, DB_NAME)
#    DB_PATH = os.path.join('/media/ramdisk', DB_NAME)
    SQLALCHEMY_DATABASE_URI = URL(drivername='sqlite', database=DB_PATH)

#    print SQLALCHEMY_DATABASE_URI


class test_config(base_config):
    """Testing configuration options."""
    TESTING = True
    WTF_CSRF_ENABLED = False

class ProductionConfig(base_config):
    DEBUG = False
    ASSETS_DEBUG = True
    WTF_CSRF_ENABLED = False
    ENV = 'prod'
    DEBUG = False
    SERVER_NAME = os.environ.get('SERVER_NAME')
    SECRET_KEY = os.environ.get('SECRET_KEY')

    MAIL_SERVER = os.environ.get('MAILCATCHER_PORT_1025_TCP_ADDR')
    MAIL_PORT = os.environ.get('MAILCATCHER_PORT_1025_TCP_PORT')

    REDIS_HOST = os.environ.get('REDIS_PORT_6379_TCP_ADDR')
    REDIS_PORT = os.environ.get('REDIS_PORT_6379_TCP_PORT')

    BROKER_URL = 'redis://{}:{}'.format(REDIS_HOST, REDIS_PORT)
    BROKER_BACKEND = BROKER_URL

    CACHE_HOST = os.environ.get('MEMCACHED_PORT_11211_TCP_ADDR')
    CACHE_PORT = os.environ.get('MEMCACHED_PORT_11211_TCP_PORT')

    POSTGRES_HOST = os.environ.get('DB_PORT_5432_TCP_ADDR')
    POSTGRES_PORT = os.environ.get('DB_PORT_5432_TCP_PORT')
    POSTGRES_USER = os.environ.get('DB_ENV_USER', 'postgres')
    POSTGRES_PASS = os.environ.get('DB_ENV_PASS', 'postgres')
    POSTGRES_DB = 'postgres'

    SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s:%s/%s' % (
        POSTGRES_USER,
        POSTGRES_PASS,
        POSTGRES_HOST,
        POSTGRES_PORT,
        POSTGRES_DB
    )

config_dict = {
    'dev': dev_config,
    'prod': ProductionConfig,
    'test': test_config,

    'default': dev_config
}

app_config = config_dict[os.getenv('APP_ENV') or 'default']
