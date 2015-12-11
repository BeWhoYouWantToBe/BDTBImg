#!/usr/bin/env python
# coding=utf-8
import re 
import pdb 
import time
import requests 
import random
from bs4 import BeautifulSoup 

class WeChat():
    def __init__(self,name):
        self.name = name 
        self.cookies_pool = []
        self.proxies = []
        self.serach_url = 'http://weixin.sogou.com/weixin?query='   
        self.cookies = {'SUID':'E2D1803D6A20900A00000000564F2FEC','SUV':'1448030190451248','SNUID':'F1C0E16B1B1F3D8FACAB4F661BA74AA7'}
        self.headers = {'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0'}

    def get_cookies(self):
        for i in range(10):
            url = self.serach_url + random.choice('abcdefghijklmnopqrstuvwxyz')
            r = requests.get(url)
            self.cookies_pool.append({'SNUID':r.cookies['SNUID'],'SUID':r.cookies['SUID']})
            time.sleep(2)

    def get_proxies(self):
        f = open('/home/emperor/Documents/proxies') 
        for p in f:
            self.proxies.append(p.strip())

    def get_gzh_url(self):
        r = requests.get(self.serach_url+self.name,cookies=self.cookies,headers=self.headers)
        soup = BeautifulSoup(r.text,'lxml') 
        url = soup.find('div',class_='wx-rb bg-blue wx-rb_v1 _item')['href']
        return 'http://weixin.sogou.com' + url 

    def get_article_url(self,gzh_url):
        i = 1
        tag = True
        article_url = []
        gzh_js = gzh_url.replace('gzh','gzhjs') + '&cb=sogou.wenxin_gzhcb&page='
        while tag:
            gzh_page = gzh_js + str(i) 
            try:
                r = requests.get(gzh_page,headers=self.headers,cookies=self.cookies)
            except:
                tag = False
            else:
                if r.url != gzh_page:
                    tag = False
                    continue
                articleUrl = re.compile(r'(?<=\[)/websearch/art.jsp.+?(?=\])').findall(r.text)
                for url in articleUrl:
                    url = 'http://weixin.sogou.com' + url
                    article_url.append(url)
                i += 1
                time.sleep(1)
        return article_url

def main():
    wechat = WeChat('我是公务员')
    pdb.set_trace()
    wechat.get_cookies()
    gzh_url = wechat.get_gzh_url() 
    print(gzh_url)
    article_url = wechat.get_article_url(gzh_url)
    print(article_url)


if __name__ == '__main__':
    main()


    

        

        
