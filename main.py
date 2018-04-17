#coding:utf-8

from flask import Flask
from flask import session
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from flask_wtf.csrf import  CSRFProtect
from flask_session import Session

app = Flask(__name__)

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
#加载配置参数
app.config.from_object(Config)
#创建连接mysql数据库的对象
db = SQLAlchemy(app)
#创建连接redis数据库的对象
redis_store = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)
#创建脚本管理器
manager = Manager(app)
#开启CSRF保护
CSRFProtect(app)
#把session数据存储到redis数据库中
Session(app)

#在迁移时让app与db产生关联
Migrate(app,db)
#将数据库迁移的脚本、命令添加到脚本管理器中
manager.add_command('db',MigrateCommand)

@app.route('/',methods=['GET','POST'])
def index():
    # redis_store.set('name','zrt')
    session['name'] = 'zrt'
    return 'index'

if __name__ == '__main__':

    manager.run()