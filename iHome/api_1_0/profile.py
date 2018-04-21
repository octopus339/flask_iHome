# -*- coding:utf-8 -*-
'个人中心'
from flask import session, jsonify

from iHome.models import User
from iHome.until.response_code import RET
from . import api
@api.route('/users',methods = ['GET'])
def get_user_info():
    """提供个人信息
    0.TODO 判断用户是否登陆
    1.从session里获取当前登陆的用户user_id
    2.查询当前登陆用户的user信息
    3.构造个人信息响应数据
    4.响应个人信息的结果
    """
    #1.从session里获取当前登陆的用户user_id
    user_id = session['user_id']
    #2.查询当前登陆用户的user信息
    try:
        user = User.query.get(user_id)
    except Exception as e:
        return jsonify(errno = RET.DBERR,errmsg = '查询用户信息失败')
    if not user:
        return jsonify(errno = RET.NODATA,errmsg = '用户不存在')
    #3.构造个人信息响应数据：响应用户的id 图片路径 用户名 手机号（定义一个字典保存）
    response_info_dict={
        'user_id':user.id,
        'avatar_url':user.avatar_url,
        'name':user.name,
        'mobile':user.mobile
    }
    #4.响应个人信息的结果
    #前端会收到这样一个字典
    """
    {
    'data':{
        'user_id':user.id,
        'avatar_url':user.avatar_url,
        'name':user.name,
        'mobile':user.mobile
    }
    'errmsg':'OK',
    }
    'errno':'0'
    }
    """

    return jsonify(errno = RET.OK,errmsg ='OK',data = response_info_dict )
