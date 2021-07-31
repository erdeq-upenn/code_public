#!/usr/bin/python
#coding=utf-8
import json
import urllib3
import requests


class iciba:
    # 初始化
    def __init__(self, wechat_config):
        self.appid = wechat_config['appid']
        self.appsecret = wechat_config['appsecret']
        self.template_id = wechat_config['template_id']
        self.access_token = ''

    # 获取access_token
    def get_access_token(self, appid, appsecret):
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (appid, appsecret)
        response = requests.get(url)
        r = response.content

        data = json.loads(r)
        access_token = data['access_token']
        self.access_token = access_token
        return self.access_token

    # 发送消息
    def send_msg(self, openid, template_id, iciba_everyday):
        msg = {
            'touser': openid,
            'template_id': template_id,
            'url': iciba_everyday['fenxiang_img'],
            'data': {
                'content': {
                    'value': iciba_everyday['content'],
                    'color': '#0000CD'
                    },
                'note': {
                    'value': iciba_everyday['note'],
                },
                'translation': {
                    'value': iciba_everyday['translation'],
                }
            }
        }
        json_data = json.dumps(msg)
        if self.access_token == '':
            self.get_access_token(self.appid, self.appsecret)
        access_token = self.access_token
        url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % str(access_token)
        request = requests.post(url, data=json_data)

        return json.loads(request.content)

    # 获取爱词霸每日一句
    def get_iciba_everyday(self):
        url = 'http://open.iciba.com/dsapi/'
        request = requests.get(url)
        data = json.loads(request.content)
        return data

    # 为设置的用户列表发送消息
    def send_everyday_words(self, openids):
        everyday_words = self.get_iciba_everyday()
        for openid in openids:
            result = self.send_msg(openid, self.template_id, everyday_words)
            if result['errcode'] == 0:
                print(' [INFO] send to %s is success' % openid)
            else:
                print(' [ERROR] send to %s is error' % openid)

    # 执行
    def run(self, openids):
        self.send_everyday_words(openids)


if __name__ == '__main__':
    # 微信配置
    wechat_config = {
        'appid': 'wxf3ff8e5699bef06a', #此处填写你的appid
        'appsecret': 'a92c42ab7c3d25e1fc1112a11cdd5377', #此处填写你的appsecret
        'template_id': 'S1uTepCZGPsJPkcKofhPLkj0Pwual8zDx31jCNhhXOQ' #此处填写你的模板消息ID
    }
    # 用户列表
    openids = [
        'odA4o6w_jyUC_Bc0HJmStNG7TaUo', #此处填写你的微信号
        #'xxxx', #如果有多个用户也可以
    #'xxxx',
    ]
    # 执行
    icb = iciba(wechat_config)
    dd = icb.get_iciba_everyday()
    icb.run(openids)
