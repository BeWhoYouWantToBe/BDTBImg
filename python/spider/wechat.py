#!/usr/bin/env python
# coding=utf-8
import re 
import os 
import pdb
import time
import requests 
import random 
from bs4 import BeautifulSoup 

def get_proxies():
    proxies = []
    f = open('/home/emperor/Documents/proxies') 
    for p in f:
       proxies.append(p.strip())
    return proxies

class WeChat():
    def __init__(self,name):
        self.name = name 
        self.proxies = {} 
        self.serach_url = 'http://weixin.sogou.com/weixin?query='   
        self.cookies = {'SUID':'E2D1803D2524920A00000000564F2FEE','SUV':'1448030190451248','SNUID':'47742598A5A18241C820FCBAA52BF8E3'}
        self.headers = {'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0'}

    
    def get_gzh_url(self):
        while True:
            r = requests.get(self.serach_url+self.name,cookies=self.cookies,headers=self.headers,proxies=self.proxies,timeout=5)
            soup = BeautifulSoup(r.text,'lxml') 
            try:
                url = soup.find('div',class_='wx-rb bg-blue wx-rb_v1 _item')['href']
                break
            except:
                self.yzm()
        return 'http://weixin.sogou.com' + url 

    def get_article_url(self,gzh_url):
        i = 1
        tag = True
        article_url = []
        gzh_js = gzh_url.replace('gzh','gzhjs') + '&cb=sogou.wenxin_gzhcb&page='
        while tag:
            gzh_page = gzh_js + str(i) 
            try:
                r = requests.get(gzh_page,headers=self.headers,cookies=self.cookies,proxies=self.proxies,timeout=5)
            except:
                tag = False
            else:
                if 'antispider' in r.url:
                    self.yzm()
                    continue
                elif 'class="logo"' in r.text:
                    tag = False 
                    continue 
                articleUrl = re.compile(r'(?<=\[)/websearch/art.jsp.+?(?=\])').findall(r.text)
                for url in articleUrl:
                    url = 'http://weixin.sogou.com' + url
                    article_url.append(url)
                i += 1
                time.sleep(5)
        return article_url 
    def get_articles(self,article_url):
        for article in article_url:
            self.save_article(article) 

    def mkdir(self):
        path = '/home/emperor//Documents/wechatgzh/' + self.name + '/'
        is_exist = os.path.exists(path)
        if not is_exist:
            os.makedirs(path) 


    def save_article(self,article_page,proxy):
        self.proxies = {'http':'http://'+proxy} 
        while True:
            try:
                r = requests.get(article_page,cookies=self.cookies,proxies=self.proxies,timeout=3)
                soup = BeautifulSoup(r.text,'lxml')
                title = soup.find('h2',{'id':'activity-name'}).string.strip()
                break
            except: 
                self.yzm()
        f = open('/home/emperor/Documents/wechatgzh/'+self.name+'/'+title,'w')
        f.write(r.text)
        f.close()
        print(title+'   已经保存完成')
        time.sleep(1)

    def yzm(self):
        proxies = get_proxies()
        if self.proxies in proxies:
            proxies.remove(self.proxies)
        self.proxies = {'http':'http://' + random.choice(proxies)}
        url = 'http://weixin.sogou.com/weixin?query=' + random.choice('abcdefghijklmnopqrstuvwxyz')
        r = requests.get(url)
        try:
            self.cookies['SNUID'] = r.cookies['SNUID']
        except:
            pass


def main():
    proxies = get_proxies()
    wechat = WeChat('我是公务员')
    wechat.yzm()
    wechat.mkdir()
    pdb.set_trace()
    gzh_url = wechat.get_gzh_url()
    article_url = wechat.get_article_url(gzh_url)
    for url in article_url:
        proxy = random.choice(proxies)
        wechat.save_article(url,proxy)


if __name__ == '__main__':
    main()


    

        

        
