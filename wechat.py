#!/usr/bin/env python
# coding=utf-8
import re 
import os 
import pdb
import time 
import random
import requests 
from queue import Queue
from threading import Thread
from bs4 import BeautifulSoup 

def get_proxy():
    proxies = []
    f = open('/home/king/Documents/proxies')
    for p in f:
        proxies.append(p.strip())
    f.close()
    return proxies

class WeChat():
    def __init__(self,name):
        self.name = name 
        self.all_proxies = [] 
        self.serach_url = 'http://weixin.sogou.com/weixin?query='   
        self.cookies = {'SUID':'8DDCFB712708930A00000000567F94DB','SUV':'1451201757470525','SNUID':'E18CA82252577AD9E18B373F531831AB'}
        self.headers = {'Accetp':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Encoding':'gzip, deflate',
               'Accept-Language':'zh-CN,en-US;q=0.7,en;q=0.3',
               'Connection':'keep-alive',
               'DNT':'1',
               'Host':'weixin.sogou.com',
               'Referer':'''http://weixin.sogou.com/gzh?openid=oIWsFt-Dzg09fQ6z65tDemuCMnOk&ext=277ZPkCeLqSVbTHD5VoBj7qT75MXs5ba
MqR5xynLyND6-5Rys_OqLC8m_pfROvED''',
               'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0'}
    
    def get_gzh_url(self):
        r = requests.get(self.serach_url+self.name,cookies=self.cookies,headers=self.headers,timeout=5)
        soup = BeautifulSoup(r.text,'lxml') 
        try:
            url = soup.find('div',class_='wx-rb bg-blue wx-rb_v1 _item')['href']
            print('获取gzhurl成功')
        except:
            print('获取gzhurl失败')
        else:
            time.sleep(8)
            return 'http://weixin.sogou.com' + url 

    def get_article_url(self,gzh_url):
        i = 1
        tag = True
        article_url = set() 
        gzh_js = gzh_url.replace('gzh','gzhjs') + '&cb=sogou.wenxin_gzhcb&page='
        while tag:
            gzh_page = gzh_js + str(i) 
            try:
                r = requests.get(gzh_page,headers=self.headers,cookies=self.cookies,timeout=5)
            except:
                tag = False 
                print('获取文章url失败')
            else:
                if 'antispider' in r.url:
                    print('触发反爬虫')
                    tag = False 
                    continue
                elif 'class="logo"' in r.text:
                    tag = False 
                    continue 
                articleUrl = re.compile(r'(?<=\[)/websearch/art.jsp.+?(?=\])').findall(r.text)
                for url in articleUrl:
                    url = 'http://weixin.sogou.com' + url 
                    article_url.add(url)
                print('获取第{}页文章url成功'.format(i))
                i += 1
                time.sleep(8)
        return article_url  

    def get_articles(self,article_url):
        for article in article_url:
            self.save_article(article) 

    def mkdir(self):
        path = '/home/king/Documents/wechatgzh/' + self.name + '/'
        is_exist = os.path.exists(path)
        if not is_exist:
            os.makedirs(path) 

    def save_article(self,article_page,proxy):
        Tag = 1
        while Tag:
            proxies = {'http':'http://'+proxy}
            try:
                r = requests.get(article_page,proxies=proxies,cookies=self.cookies,timeout=8)
            except:
                proxy = self.change_proxy()
            else:
                soup = BeautifulSoup(r.text,'lxml')
                try:
                    title = soup.find('h2',{'id':'activity-name'}).string.strip()
                except:
                    proxy = self.change_proxy() 
                else:
                    Tag = 0
        
        f = open('/home/king/Documents/wechatgzh/'+self.name+'/'+title,'w')
        f.write(r.text)
        f.close()
        print(title+'   已经保存完成')
        time.sleep(8)

    def change_proxy(self):
        return  random.choice(self.all_proxies[10:-1])
    


def main():
    wechat = WeChat('我是公务员')
    wechat.mkdir()
    wechat.all_proxies = get_proxy()
    gzh_url = wechat.get_gzh_url()
    article_url = wechat.get_article_url(gzh_url)
    pdb.set_trace()
    q = Queue()
    NUM = 10 
    def run(proxy):
        while 1:
            url = q.get() 
            wechat.save_article(url,proxy)
            q.task_done() 
    for i in range(NUM):
        proxy = wechat.all_proxies[i]
        t = Thread(target=run,args=(proxy,)) 
        t.setDaemon(True) 
        t.start() 
    for url in article_url:
        q.put(url) 
    q.join()
    print('全部完成')

if __name__ == '__main__':
    main()


    

        

        
