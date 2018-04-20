# -*- coding:utf-8 -*-
import re

from flask import request, jsonify,current_app
from iHome.until.response_code import RET
from iHome import redis_store, db
from iHome.models import User

from . import api
@api.route('/users',methods=['POST'])
def register():
    """
    注册
    1.获取用户的手机号码 密码 短信验证码
    2.判断参数是否缺少
    3.获取服务器存储的验证码
    4.服务器的验证码与客户端的验证码进行对比
    5.如果对比成功，则创建用户模型User对象，并给属性赋值
    6.将属性写入数据库
    7.响应注册结果

    """
    #获取用户的手机号码 密码 短信验证码
    #有3种方法获取前端ajax发来的json字符串
    #1.    # json_str = request.data
            # json_dict = json.loads(json_str)
    #下面两种要确保发来的数据是json字符串
    #2.json_dict = request.get_json()
    #第3种
    json_dict = request.json

    mobile = json_dict.get('mobile')
    sms_code_client = json_dict.get('sms_code')
    passwoed = json_dict.get('passwoed')

    #2.判断参数是否缺少
    if not all([mobile,sms_code_client,passwoed]):
        return jsonify(errno = RET.PARAMERR,errmsg = '缺少参数')
    if not re.match(r'^1[3456789][0-9]{9}$',mobile):
        return jsonify(errno = RET.PARAMERR,errmsg = '手机格式错误')


    #3.获取服务器存储的验证码
    try:
     sms_code_server = redis_store.get('SMS:%s'%mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.DBERR,errmsg = '查询短信验证码失败')
    if not sms_code_server:
        return jsonify(errno = RET.NODATA,errmsg = '短信验证码不存在')
    #4.服务器的验证码与客户端的验证码进行对比
    if sms_code_client != sms_code_server:
        return jsonify(errno = RET.PARAMERR,errmsg = '短信验证码输出错误')

    #5.如果对比成功，则创建用户模型User对象，并给属性赋值
    user = User()
    user.mobile = mobile
    user.name  = mobile
    #TODO 密码需要加密后再保存到数据库
    #6.将属性写入数据库
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno = RET.DBERR,errmsg = '保存用户信息失败')
    #7.响应注册结果
    return jsonify(errno = RET.OK,errmsg = '注册成功')






