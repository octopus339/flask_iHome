#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from iHome.yuntongxun.CCPRestSDK import REST
import ConfigParser

#主帐号
accountSid= '8a216da862dcd1050162de1398780125'

#主帐号Token
accountToken= '795857a9a4ce4105a20b387a5740191a'

#应用Id
appId='8a216da862dcd1050162de1398d3012b'

#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com'

#请求端口 
serverPort='8883';

#REST版本号
softVersion='2013-12-26';

class CCP(object):
    #封装一个单例，用于统一发送短信验证码
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'_instance'):
            cls._instance = super(CCP,cls).__new__(cls, *args, **kwargs)
           #初始化REST SDK
            cls._instance.rest = REST(serverIP,serverPort,softVersion)
            cls._instance.rest.setAccount(accountSid,accountToken)
            cls._instance.rest.setAppId(appId)
        return cls._instance
    def send_sms_code(self,to, datas, tempId):
        #发送短信验证码的方法
        #result 会返回smsMessageSid  dateCreated   statusCode三个字典格式的数据
        result = self.rest.sendTemplateSMS(to, datas, tempId)
        #判断短信是否发送成功，如果发送成功statusCode：000000
        if result.statusCode == '000000':
            #这里返回的值给调用者判断短信是否发送成功
            return 1
        else:
            return 0


  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
  # @param $tempId 模板Id

# def sendTemplateSMS(to,datas,tempId):
#
#
#     #初始化REST SDK
#     rest = REST(serverIP,serverPort,softVersion)
#     rest.setAccount(accountSid,accountToken)
#     rest.setAppId(appId)
#
#     result = rest.sendTemplateSMS(to,datas,tempId)
#     for k,v in result.iteritems():
#
#         if k=='templateSMS' :
#                 for k,s in v.iteritems():
#                     print '%s:%s' % (k, s)
#         else:
#             print '%s:%s' % (k, v)
#
#
# sendTemplateSMS('13360226175',['leslie','5'],1)