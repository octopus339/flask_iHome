# -*- coding:utf-8 -*-
from flask import Flask
from flask_wtf.csrf import  CSRFProtect
from flask_session import Session
from config import configs
from flask_sqlalchemy import SQLAlchemy
import redis
from iHome.until.common import RegexConverter
db = SQLAlchemy()

redis_store = None
def get_app(config_name):
    app = Flask(__name__)

    #加载配置参数
    app.config.from_object(configs[config_name])
    #创建连接mysql数据库的对象
    db.init_app(app)

    #创建连接redis数据库的对象
    global redis_store
    redis_store = redis.StrictRedis(host=configs[config_name].REDIS_HOST,port=configs[config_name].REDIS_PORT)

    #开启CSRF保护
    CSRFProtect(app)
    #把session数据存储到redis数据库中
    Session(app)
    app.url_map.converters['re'] = RegexConverter
    from iHome.api_1_0 import api
    app.register_blueprint(api)
    from iHome.web_html import html_blue
    app.register_blueprint(html_blue)
    return app