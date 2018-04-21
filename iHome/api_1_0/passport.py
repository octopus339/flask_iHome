# -*- coding:utf-8 -*-
import re

from flask import request, jsonify,current_app
from flask import session

from iHome.until.response_code import RET
from iHome import redis_store, db
from iHome.models import User

from . import api
@api.route('/session',methods = ['POST'])
def login():
    """
    登陆
    1.接收登陆参数：手机号  密码
    2.判断参数是否为空，并校验手机号的格式
    3.使用手机号查询用户信息
    4.对比用户的密码
    5.写入状态保持信息到session
    6.响应登陆结果
    """
    #1.接收登陆参数：手机号  密码
    json_dict = request.json
    mobile = json_dict.get('mobile')
    password = json_dict.get('password')
    #2.判断参数是否为空，并校验手机号的格式
    if not all([mobile,password]):
        return jsonify(errno = RET.PARAMERR,errmsg = '参数错误')
    if not re.match(r'^1[3456789][0-9]{9}$',mobile):
        return jsonify(errno = RET.PARAMERR,errmsg = '手机格式错误')
    #3.使用手机号查询用户信息
    try:
        user = User.query.filter(User.mobile==mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.DBERR,errmsg = '查询用户数据失败')
    #这里主要是用户名错误，但为了安全要打印用户名或者密码错误迷惑黑客
    if not user:
        return jsonify(errno = RET.NODATA,errmsg = '用户名或者密码错误')
    #4.对比用户的密码，要先在modles定义一个check_password_hash方法把数据库的密码解密
    if not user.check_password(password):
        return jsonify(errno = RET.NODATA,errmsg = '用户名或者密码错误')
    #5.写入状态保持信息到session
    session['user_id'] = user.id
    session['user_name'] = user.name


    #6.响应登陆结果
    return jsonify(errno = RET.OK,errmsg = '登陆成功')







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
    password = json_dict.get('password')

    #2.判断参数是否缺少
    if not all([mobile,sms_code_client,password]):
        return jsonify(errno = RET.PARAMERR,errmsg = '缺少参数')
    if not re.match(r'^1[3456789][0-9]{9}$',mobile):
        return jsonify(errno = RET.PARAMERR,errmsg = '手机格式错误')


    #3.获取服务器存储的验证码
    try:
     sms_code_server = redis_store.get('SMS:%s'%mobile)
     current_app.logger.debug(sms_code_server)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.DBERR,errmsg = '查询短信验证码失败')
    if not sms_code_server:
        return jsonify(errno = RET.NODATA,errmsg = '短信验证码不存在')
    #4.服务器的验证码与客户端的验证码进行对比
    if sms_code_client != sms_code_server:
        return jsonify(errno = RET.PARAMERR,errmsg = '短信验证码输出错误')
    #判断手机后是否已经存在
    if User.query.filter(User.mobile == mobile).first():
        return jsonify(errno = RET.DATAEXIST,errmsg = '该手机号已经存在')

    #5.如果对比成功，则创建用户模型User对象，并给属性赋值
    user = User()
    user.mobile = mobile
    user.name  = mobile

    #需要将密码加密后保存到数据库：调用password属性的setter方法
    user.password= password
    #6.将属性写入数据库
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno = RET.DBERR,errmsg = '保存用户信息失败')
    session['user_id'] = user.id
    session['user_name'] = user.name
    #7.响应注册结果
    return jsonify(errno = RET.OK,errmsg = '注册成功')






