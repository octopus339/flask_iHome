# -*- coding:utf-8 -*-
from flask import session, jsonify
from werkzeug.routing import BaseConverter

from iHome.until.response_code import RET
from functools import wraps


class RegexConverter(BaseConverter):
    def __init__(self,url_map,*args):
        super(RegexConverter,self).__init__(url_map)
        self.regex = args[0]


#view_func接收被装饰的函数
def login_required(view_func):
    #用装饰器装饰函数要加上@wraps(接收装饰器装饰的函数的参数)
    @wraps(view_func)
    def wraaper(*args,**kwargs):
        #具体实现判断用户是否登陆逻辑
        user_id = session.get('user_id')
        if not user_id:
            return jsonify(errno = RET.SESSIONERR,errmsg = '用户未登陆')
        else:
            #实际是调用杯装饰的函数，即装饰器下的函数
            return view_func(*args,**kwargs)
    return wraaper
