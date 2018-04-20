# -*- coding:utf-8 -*-
import logging
import random
import re

from flask import abort, jsonify
from flask import current_app
from flask import json

from iHome.until.captcha.captcha import captcha
from iHome.until.sms import CCP
from . import api
from flask import make_response,request
from iHome import redis_store
from iHome.until.response_code import RET
from iHome import constants

@api.route('/sms_code',methods=['POST'])
def send_sms_code():
    """发送验证码
    1.获取用户输入的手机号 验证码 uuid
    2.判断获取的参数不为空，并校验手机号
    3.获取数据库中存储的验证码text
    4.用用户输入的验证码与数据库中的验证码对比
    5.对比成功后生成短信验证码
    6. 调用单例发送短信验证码
    7.如果短信验证码发送成功，则把短信验证码保存到redis数据库
    8.响应发送短信的结果
    """
    #1.获取用户输入的手机号 验证码 uuid
    #因为前端传过来的值是json格式的字符串，所以用data接收
    json_str = request.data
    #将json格式的字符串转为字典格式获取手机号 验证码 uuid
    json_dict = json.loads(json_str)
    mobile = json_dict.get('mobile')
    imageCode_client = json_dict.get('imageCode')
    uuid = json_dict.get('uuid')
    #2.判断获取的参数不为空，并校验手机号
    #判断参数是否存在
    if not all([mobile,imageCode_client,uuid]):
        return jsonify(errno = RET.PARAMERR,errmsg = '缺少参数' )
    #判断手机格式是否正确
    if not re.match(r'^1[345678][0-9]{9}$',mobile):
        return jsonify(errno = RET.PARAMERR,errmsg = '手机号错误' )
    #3.获取数据库中存储的验证码text
    try:
        imageCode_server = redis_store.get('ImageCode:%s'%uuid)

    except Exception as e:
        return jsonify(errno = RET.DBERR,errmsg = '查询验证码失败')
    if not imageCode_server:
        return jsonify(errno = RET.NODATA,errmsg = '验证码不存在')
    #4.用用户输入的验证码与数据库中的验证码对比
    if imageCode_client.lower() != imageCode_server.lower():
        return jsonify(errno = RET.PARAMERR,errmsg = '输入的验证码错误')
    #5.对比成功后生成短信验证码
    sms_code = '%06d'%random.randint(0,999999)

    #6. 调用单例发送短信验证码
    result = CCP().send_sms_code(mobile,[sms_code,constants.SMS_CODE_REDIS_EXPIRES/60],'1')
    if result != 1:
        return jsonify(errno = RET.THIRDERR,errmsg = '短信验证码发送失败')
    #7.如果短信验证码发送成功，则把短信验证码保存到redis数据库
    try:
        redis_store.set('SMS:%s'%mobile,sms_code,constants.SMS_CODE_REDIS_EXPIRES)

    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(errno = RET.DBERR,errmsg = '存储短信验证码失败')

    #8.响应发送短信的结果
    return jsonify(errno = RET.OK,errmsg = '发送短信验证码成功')




#定义变量记录上一次的uuid
last_uuid = ''
@api.route('/image_code',methods=['GET'])
def get_image_code():
    #1.接收html定义的uuid值，并校验uuid
    uuid = request.args.get('uuid')
    if not uuid:
        abort(403)
    #2.生成图片验证码
    name,text,image = captcha.generate_captcha()
    current_app.logger.debug(text)
    #debug只能在测试模式下使用
    #logging.debug(text)

    # current_app.logger.warning(text)

    #3.使用redis数据库存储图片验证码，ImageCode：uuid作为key
    try:
        if uuid:
            redis_store.delete('ImageCode:%s'%last_uuid)
        redis_store.set('ImageCode:%s'%uuid,text,constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        print e
        #有可能使服务器崩溃的警报，线上要用error模式
        # logging.error(e)
        #两种显示日志方法都可以使用
        current_app.logger.error(e)

        return jsonify(errno=RET.DBERR,errmsg = '存储验证码错误')
    #记录当前uuid，方便下一次使用时作为上一次的uuid，删除text
    global last_uuid
    last_uuid = uuid
    #4.响应图片验证码
    #修改响应头的信息，指定响应内容是image.jpg
    respone = make_response(image)
    respone.headers['Content-Type'] = 'image.jpg'
    return respone
