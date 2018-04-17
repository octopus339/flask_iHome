# -*- coding:utf-8 -*-
import redis
class Config(object):
    """配置参数"""
    DEBUG =True
    SECRET_KEY = 'python'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/iHome01'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #配置redis数据库，实际开发使用redis数据库的真实ip
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    #配置session参数
    #指定session存储到redis数据库中
    SESSION_TYPE = 'redis'
    #指定redis的位置
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    #是否使用secret_key签名session_data
    SESSION_USE_SIGNER = True
    #设置session的过期时间
    PERMANENT_SESSION_LIFETIME = 3600 * 24  # 有效期为一天
class Dev(Config):
    pass
class Pro(Config):
    DEBUG = False
class UnitTest(Config):
    TESTING = True
configs = {
    'dev':Dev,
    'pro':Pro,
    'test':UnitTest
}