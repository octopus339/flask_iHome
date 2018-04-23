# -*- coding:utf-8 -*-
from celery import current_app
from flask import jsonify

from iHome.api_1_0 import api
from iHome.models import Area
from iHome.until.response_code import RET


@api.route('/areas',methods = ['GET'])
def get_areas():
    """提供城区信息
    1.直接查询所有城区信息
    2.构造城区信息响应数据
    3.响应城区信息
    """
    # 1.直接查询所有城区信息areas == [Area,Area,Area...]
    try:
        areas = Area.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.DBERR,errmsg = '查询城区信息失败')
    #2.构造城区信息响应数据:将areas转成字典列表
    area_list = []
    for area in areas:
        area_list.append(area.to_dict())
    #3.响应城区信息：只认得字典或者字典或列表
    return jsonify(errno = RET.OK,errmsg = 'OK',data = area_list)
