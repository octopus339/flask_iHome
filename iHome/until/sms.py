#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from iHome.yuntongxun.CCPRestSDK import REST
import ConfigParser

#���ʺ�
accountSid= '8a216da862dcd1050162de1398780125'

#���ʺ�Token
accountToken= '795857a9a4ce4105a20b387a5740191a'

#Ӧ��Id
appId='8a216da862dcd1050162de1398d3012b'

#�����ַ����ʽ���£�����Ҫдhttp://
serverIP='app.cloopen.com'

#����˿� 
serverPort='8883';

#REST�汾��
softVersion='2013-12-26';

class CCP(object):
    #��װһ������������ͳһ���Ͷ�����֤��
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'_instance'):
            cls._instance = super(CCP,cls).__new__(cls, *args, **kwargs)
           #��ʼ��REST SDK
            cls._instance.rest = REST(serverIP,serverPort,softVersion)
            cls._instance.rest.setAccount(accountSid,accountToken)
            cls._instance.rest.setAppId(appId)
        return cls._instance
    def send_sms_code(self,to, datas, tempId):
        #���Ͷ�����֤��ķ���
        #result �᷵��smsMessageSid  dateCreated   statusCode�����ֵ��ʽ������
        result = self.rest.sendTemplateSMS(to, datas, tempId)
        #�ж϶����Ƿ��ͳɹ���������ͳɹ�statusCode��000000
        if result.statusCode == '000000':
            #���ﷵ�ص�ֵ���������ж϶����Ƿ��ͳɹ�
            return 1
        else:
            return 0


  # ����ģ�����
  # @param to �ֻ�����
  # @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
  # @param $tempId ģ��Id

# def sendTemplateSMS(to,datas,tempId):
#
#
#     #��ʼ��REST SDK
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