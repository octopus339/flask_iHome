# -*- coding:utf-8 -*-
'个人中心'
from celery import current_app
from flask import request,g
from flask import session, jsonify

from iHome import db, constants
from iHome.models import User
from iHome.until.common import login_required
from iHome.until.response_code import RET
from . import api
from iHome.until.image_storage import upload_image

@api.route('/users/auth',methods = ['GET'])
@login_required
def get_user_auth():
    """提供实名认证数据
    0.判断用户是否登陆
    1.查询当前用的user信息
    2.构造响应实名认证的数据
    3.响应实名认证的数据
    """
    #1.查询当前用的user信息
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.DBERR,errmsg = '查询用户信息失败')
    if not user:
        return jsonify(errno = RET.NODATA,errmsg = '用户不存在')
    #2.构造响应实名认证的数据
    response_auth_dict = user.auth_to_dict()

    #3.响应实名认证的数据
    return jsonify(errno = RET.OK,errmsg = 'OK',data = response_auth_dict)




@api.route('/users/auth',methods = ['POST'])
@login_required
def set_user_auth():
    """实名认证
    0.判断用户是否登陆
    1.获取用户实名参数：real_name,id_card,并判断参数不为空
    2.查询当前用户的user模型
    3.把real_name,id_card赋值给user模型
    4.保存到数据库
    5.响应认证结果
    """
    #1.获取用户实名参数：real_name,id_card,并判断参数不为空
    json_dict  = request.json
    real_name = json_dict.get('real_name')
    id_card = json_dict.get('id_card')
    if not all([real_name,id_card]):
        return jsonify(errno = RET.PARAMERR,errmsg = '缺少参数')
    #2.查询当前用户的user模型
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.DBERR,errmsg = '查询用户数据失败')
    if not user:
        return jsonify(errno = RET.PARAMERR,errmsg = '用户不存在')
    #3.把real_name,id_card赋值给user模型
    user.real_name = real_name
    user.id_card = id_card
    #4.保存到数据库
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno = RET.DBERR,errmsg = '认证信息保存失败')
    #5.响应认证结果
    return jsonify(errno = RET.OK,errmsg = '用户认证成功')



@api.route('/users/name',methods = ['PUT'])
@login_required
def set_user_name():
    """
    修改用户名
    0.判断用户是否登陆
    1.获取新的用户名，判断是否为空
    2.查询当前用户名
    3.将新的用户名赋值给当前的登陆用户的user模型
    4.将数据保存到数据库
    5.响应修改用户名的结果
    """
    #1.获取新的用户名，判断是否为空
    new_name = request.json.get('name')
    if not new_name:
        return jsonify(errno = RET.PARAMERR,errmsg = '缺少参数')
    #2.查询当前用户名
    # user_id = session['user_id']
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.DBERR,errmsg = '查询用户失败')
    if not user:
        return jsonify(errno = RET.PARAMERR,errmsg = '用户不存在')
    #3.将新的用户名赋值给当前的登陆用户的user模型

    user.name = new_name
    #4.将数据保存到数据库
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno = RET.DBERR,errmsg = '保存用户失败')
    #5.响应修改用户名的结果
    return jsonify(errno = RET.OK,errmsg = '修改用户名成功')





@api.route('/users/avatar')
@login_required
def upload_avatar():
    """
    上传用户头像
    0.TODO判断用户是否登陆
    1.获取用户上传的头像数据并校验
    2.查询当前登陆用户
    3.调用上传工具方法实现用户头像上传
    4.把用户上传的头像数据传到当前登陆用户的user模型
    5.把数据保存到数据库
    6.响应上传用户头像的结果
    """
    #1.获取用户上传的头像数据并校验
    try:
        avatar_data = request.files.get('avatar')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.PARAMERR,errmsg = '获取用户上传的图片失败')
    #2.查询当前登陆用户
    # user_id = session['user_id']
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.DBERR,errmsg = '查询用户信息失败')
    if not user:
        return jsonify(errno = RET.PARAMERR,errmsg = '用户不存在')
    #3.调用上传工具方法实现用户头像上传
    try:
        key = upload_image(avatar_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.THIRDERR,errmsg = '上传用户头像失败')
    #4.把用户上传的头像数据传到当前登陆用户的user模型
    user.avatar_url = key
    #5.把数据保存到数据库
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno = RET.DBERR,errmsg = '保存用户头像失败')
    #6.响应上传用户头像的结果
    #因为http://oyucyko3w.bkt.clouddn.com/是配置信息所以写到constants
    # avatar_url = 'http://oyucyko3w.bkt.clouddn.com/' + key
    avatar_url = constants.QINIU_DOMIN_PREFIX + key
    return jsonify(errno = RET.OK,errmsg = '上传用户头像成功',data = avatar_url)





@api.route('/users',methods = ['GET'])
@login_required
def get_user_info():
    """提供个人信息
    0.TODO 判断用户是否登陆
    1.从session里获取当前登陆的用户user_id
    2.查询当前登陆用户的user信息
    3.构造个人信息响应数据
    4.响应个人信息的结果
    """
    #1.从session里获取当前登陆的用户user_id
    # user_id = session['user_id']
    user_id = g.user_id
    #2.查询当前登陆用户的user信息
    try:
        user = User.query.get(user_id)
    except Exception as e:
        return jsonify(errno = RET.DBERR,errmsg = '查询用户信息失败')
    if not user:
        return jsonify(errno = RET.NODATA,errmsg = '用户不存在')
    #3.构造个人信息响应数据：响应用户的id 图片路径 用户名 手机号（定义一个字典保存）
    response_info_dict= user.to_dict()
    #4.响应个人信息的结果
    #前端会收到这样一个字典

    # {
    # 'data':{
    #     'user_id':user.id,
    #     'avatar_url':user.avatar_url,
    #     'name':user.name,
    #     'mobile':user.mobile
    # }
    # 'errmsg':'OK',
    # }
    # 'errno':'0'
    # }


    return jsonify(errno = RET.OK,errmsg ='OK',data = response_info_dict )
