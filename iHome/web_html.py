# -*- coding:utf-8 -*-
from flask import Blueprint,current_app
html_blue = Blueprint('html',__name__)

@html_blue.route('/<re(".*"):file_name>')
def show_html(file_name):
    if not file_name:
        file_name = 'index.html'
    file_name = 'html/%s'%file_name
    return current_app.send_static_file(file_name)