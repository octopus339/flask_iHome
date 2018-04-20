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

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
  # @param $tempId 模板Id

def sendTemplateSMS(to,datas,tempId):

    
    #初始化REST SDK
    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)
    
    result = rest.sendTemplateSMS(to,datas,tempId)
    for k,v in result.iteritems(): 
        
        if k=='templateSMS' :
                for k,s in v.iteritems(): 
                    print '%s:%s' % (k, s)
        else:
            print '%s:%s' % (k, v)
    
   
sendTemplateSMS('13360226175',['leslie','5'],1)