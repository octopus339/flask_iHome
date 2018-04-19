# -*- coding:utf-8 -*-
from flask import abort, jsonify

from iHome.until.captcha.captcha import captcha
from . import api
from flask import make_response,request
from iHome import redis_store
from iHome.until.response_code import RET
from iHome import constants

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
    #3.使用redis数据库存储图片验证码，ImageCode：uuid作为key
    try:
        if uuid:
            redis_store.delete('ImageCode:%s'%last_uuid)
        redis_store.set('ImageCode:%s'%uuid,text,constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        print e
        return jsonify(errno=RET.DBERR,errmsg = '存储验证码错误')
    #记录当前uuid，方便下一次使用时作为上一次的uuid，删除text
    global last_uuid
    last_uuid = uuid
    #4.响应图片验证码
    #修改响应头的信息，指定响应内容是image.jpg
    respone = make_response(image)
    respone.headers['Content-Type'] = 'image.jpg'
    return respone
