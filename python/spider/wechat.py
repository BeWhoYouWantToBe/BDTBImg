#!/usr/bin/env python
# coding=utf-8
import re 
import pdb
import requests
from bs4 import BeautifulSoup 

class WeChat():
    def __init__(self,name):
        self.name = name 
        self.serach_url = 'http://weixin.sogou.com/weixin?type=1&query=' + name   
        self.headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 4.4.2; sdk Build/KK) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 MicroMessenger/6.0.0.61_r920612.501 NetType/epc.tmobile.com'}
        self.proxies = []

    def get_proxies(self):
        f = open('/home/emperor/Documents/proxies') 
        for p in f:
            self.proxies.append(p.strip())
    def get_gzh_url(self):
        i = 0
        while True:
            proxy = self.proxies[i]
            proxies ={'http':'http://'+proxy}
            r = requests.get(self.serach_url,headers=self.headers,proxies=proxies)
            soup = BeautifulSoup(r.text,'lxml') 
            url = soup.find('div',class_='wx-rb bg-blue wx-rb_v1 _item')['href']
            if url:
                return 'http://weixin.sogou.com' + url 
            else:
                i += 1
    def get_article_url(self,gzh_url):
        i = 1
        tag = True
        article_url = []
        gzh_js = gzh_url.replace('gzh','gzhjs') + '&cb=sogou.wenxin_gzhcb&page='
        while tag:
            gzh_js = gzh_js + str(i) 
            try:
                r = requests.get(gzh_js)
            except:
                tag = False
            else:
                articleUrl = re.compile(r'(?<=\[)/websearch/art.jsp.+?(?=\])').findall(r.text)
                for url in articleUrl:
                    url = 'http://weixin.sogou.com' + url
                    article_url.append(url)
                i += 1

def main():
    wechat = WeChat('我是公务员')
    wechat.get_proxies()
    gzh_url = wechat.get_gzh_url() 
    article_url = wechat.get_article_url(gzh_url)
    print(article_url)


if __name__ == '__main__':
    main()


    

        

        
