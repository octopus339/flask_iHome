# -*- coding:utf-8 -*-
from flask import Blueprint,current_app
html_blue = Blueprint('html',__name__)

@html_blue.route('/<file_name>')
def show_html(file_name):
    file_name = 'html/%s'%file_name
    return current_app.send_static_file(file_name)