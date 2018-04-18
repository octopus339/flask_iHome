# -*- coding:utf-8 -*-
from iHome.until.captcha.captcha import captcha
from . import api
from flask import make_response
@api.route('/image_code',methods=['GET'])
def get_image_code():
    name,text,image = captcha.generate_captcha()
    respone = make_response(image)
    respone.headers['Content-Type'] = 'image.jpg'
    return respone
