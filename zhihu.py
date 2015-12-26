#!/usr/bin/env python
# coding=utf-8
import re 
import os  
import pdb
import requests 
import random
from bs4 import BeautifulSoup

class zhihuClient:
    def __init__(self):
        self.login_url = 'https://www.zhihu.com/login/email'
        self.cookies = {}
        self.session = requests.session() 
        self.headers = {'Host':'www.zhihu.com',
        'Referer':'https://www.zhihu.com/',
        'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0'}

    def get_captcha(self):
        url = 'https://www.zhihu.com/captcha.gif?r=' + str(random.randint(1,99999999999999))
        r = self.session.get(url,headers=self.headers)
        f = open('/home/king/captcha','wb')
        f.write(r.content) 
        f.close()
        os.system('eog /home/king/captcha')
        os.remove('/home/king/captcha')
        captcha = input('请输入验证码：')
        return captcha

    def login(self):
        print('===== login =====') 
        pdb.set_trace()
        email = input('email:')
        password = input('password:')
        captcha = self.get_captcha()
        data = {'remember_me':'true','email':email,'password':password,'captcha':captcha}
        r = self.session.post(self.login_url,data=data,headers=self.headers) 
        print('===== logging... =====') 
        code = r.json()['r'] 
        if code == '0':
            print('login successful')
        else:
            print('login failed')
        self.cookies = r.cookies.get_dict()


if __name__=='__main__':
    zhihuClient = zhihuClient()
    zhihuClient.login()

        


        


