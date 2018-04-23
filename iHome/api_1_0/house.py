# -*- coding:utf-8 -*-
from celery import current_app
from flask import jsonify,g
from flask import request

from iHome import db
from iHome.api_1_0 import api
from iHome.models import Area, House, Facility
from iHome.until.common import login_required
from iHome.until.response_code import RET

@api.route('/houses', methods=['POST'])
@login_required
def pub_house():
    """
    发布新的房源
    0.判断用户是否登录
    1.接受参数：基本信息和设备信息
    2.判断参数是否为空，并对某些参数进行合法性的校验,比如金钱相关的
    3.创建房屋模型对象，并赋值
    4.保存房屋数据到数据库
    5.响应发布新的房源的结果
    """
    #1.接受参数：基本信息和设备信息
    json_dict = request.json
    title = json_dict.get('title')
    price = json_dict.get('price')
    address = json_dict.get('address')
    area_id = json_dict.get('area_id')
    room_count = json_dict.get('room_count')
    acreage = json_dict.get('acreage')
    unit = json_dict.get('unit')
    capacity = json_dict.get('capacity')
    beds = json_dict.get('beds')
    deposit = json_dict.get('deposit')
    min_days = json_dict.get('min_days')
    max_days = json_dict.get('max_days')
    facility = json_dict.get('facility') # [2,4,6,8,10]
    #2.判断参数是否为空，并对某些参数进行合法性的校验,比如金钱相关的
    if not all([title, price, address, area_id, room_count, acreage, unit, capacity, beds, deposit, min_days, max_days, facility]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')
    #校验价格和押金是否合法，不允许传入数字以外的数据
    #在涉及关于金钱的开发中把数字*100把元转为分，显示的时候再除以100转为元
    #  10元 * 100 == 1000 分
    # 10.1元 * 100 == 1010分
    try:
        price = int(float(price)*100)
        deposit = int(float(deposit) * 100)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='金额格式错误')
    #3.创建房屋模型对象，并赋值
    house = House()
    house.user_id = g.user_id
    house.area_id = area_id
    house.title = title
    house.price = price
    house.address = address
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.deposit = deposit
    house.min_days = min_days
    house.max_days = max_days
    # 给facilities属性赋值，实现多对多的关联关系 facility == [2,4,6,8,10]
    facilities = Facility.query.filter(Facility.id.in_(facility)).all()
    house.facilities = facilities


    #4.保存房屋数据到数据库
    try:
        db.session.add(house)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存房屋数据失败')

    # 5.响应发布新的房源的结果
    return jsonify(errno=RET.OK, errmsg='发布新房源成功')





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
