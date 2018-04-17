#coding:utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from flask_wtf.csrf import  CSRFProtect

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

#加载配置参数
app.config.from_object(Config)
#创建连接mysql数据库的对象
db = SQLAlchemy(app)
#创建连接redis数据库的对象
redis_store = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)
#创建脚本管理器
manager = Manager(app)
CSRFProtect(app)
#在迁移时让app与db产生关联
Migrate(app,db)
#将数据库迁移的脚本、命令添加到脚本管理器中
manager.add_command('db',MigrateCommand)

@app.route('/',methods=['GET','POST'])
def index():
    # redis_store.set('name','zrt')
    return 'index'

if __name__ == '__main__':

    manager.run()