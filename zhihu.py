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
        self.headers = {'Host': 'www.zhihu.com',
                        'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0',
                       'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                        }

    def get_captcha(self):
        url = 'https://www.zhihu.com/captcha.gif?r=' + \
            str(random.randint(1, 99999999999999))
        r = self.session.get(url, headers=self.headers)
        f = open('/home/king/captcha', 'wb')
        f.write(r.content)
        f.close()
        os.system('eog /home/king/captcha')
        os.remove('/home/king/captcha')
        captcha = input('请输入验证码：')
        return captcha

    def login(self):
        print('===== login =====')
        email = input('email:')
        password = input('password:')
        captcha = self.get_captcha()
        data = {
            'remember_me': 'true',
            'email': email,
            'password': password,
            'captcha': captcha}
        r = self.session.post(self.login_url, data=data, headers=self.headers)
        print('===== logging... =====')
        msg = r.json()['msg']
        if msg == '登陆成功':
            print('login successful')
        else:
            print('login failed')
            print(msg)
        self.cookies = r.cookies.get_dict()

    def get_content(self):
        pdb.set_trace()
        content = {}
        s = self.session.get('https://www.zhihu.com', headers=self.headers)
        soup = BeautifulSoup(s.content,'lxml')
        content_tag = soup.find_all(lambda div:'class' in div.attrs and div['class']=='content' and len(list(div.children))==5)
        return content
            
        
        


if __name__ == '__main__':
    zhihuClient = zhihuClient()
    zhihuClient.login()
    content = zhihuClient.get_content()
    for c in content:
        print(c+':'+content[c]+'\n')
