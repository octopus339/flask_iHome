# -*- coding:utf-8 -*-
from flask import Blueprint,current_app,make_response
from flask_wtf.csrf import generate_csrf

html_blue = Blueprint('html',__name__)

@html_blue.route('/<re(".*"):file_name>')
def show_html(file_name):
    if not file_name:
        file_name = 'index.html'
    if file_name != 'favicon.ico':
        file_name = 'html/%s'%file_name
    response  = make_response(current_app.send_static_file(file_name))
    #生成一个csrf_token
    csrf_token = generate_csrf()
    #将csrf_token写进cookie
    response.set_cookie('csrf_token',csrf_token)

    return response