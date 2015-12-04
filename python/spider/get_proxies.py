#!/usr/bin/env python
# coding=utf-8
import re 
import pdb
import requests 
from queue import Queue
from threading import Thread
from bs4 import BeautifulSoup 

def get_sakura_ne_jp(l):
    mode,arg1,arg2,arg3,arg4,port = l
    mode = int(mode)
    if mode == 1:
        return arg1+"."+arg2+"."+arg3+"."+arg4+":"+port
    elif mode == 2:
        return arg4+"."+arg1+"."+arg2+"."+arg3+":"+port
    elif mode == 3:
        return arg3+"."+arg4+"."+arg1+"."+arg2+":"+port
    elif mode == 4:
        return arg2+"."+arg3+"."+arg4+"."+arg1+":"+port

class proxy():
    def __init__(self,urls,dir):
        self.urls = urls 
        self.dir = dir 
        self.proxies_list = []
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    def spider(self):
        proxies = set() 
        for url in self.urls:
            r = requests.get(url,headers=self.headers) 
            soup = BeautifulSoup(r.text,'lxml') 
            if url == self.urls[0]:
                proxy = soup.find_all('td',text=re.compile(':')) 
                for p in proxy:
                    proxies.add(p.string)
            elif url == self.urls[1]:
                proxy = []
                pro = soup.find_all(text=re.compile(r'\d{1,3}\.'))
                for p in pro:
                    proxy.append(p[1:])
                proxy[0] = pro[0]
                proxies.update(proxy)
            elif url == self.urls[2]:
                proxy = []
                span = soup.find_all('span',text=re.compile(r':')) 
                css_url = 'http://www.samair.ru' + soup.find('link',href=re.compile(r'/styles/\w+\.css'))['href']
                ports = requests.get(css_url,headers=self.headers) 
                ports_soup = BeautifulSoup(ports.text,'lxml') 
                body = ports_soup.body.string.split('\n')[:-1]
                port = {} 
                for b in body:
                    temp = re.split(r'[\.:"]',b)
                    port[temp[1]] = temp[-2]
                for p in span:
                    proxy.append(p.string+port[p['class'][0]])
                proxies.update(proxy)    
            elif url == self.urls[3]:
                args = soup.find_all(text=re.compile(r'\(\d\,'))
                proxy = []
                for arg in args:
                    proxy.append(get_sakura_ne_jp(arg.lstrip("\\n<!--\nproxy(").rstrip(');\n// -->\n').split(',')).replace("'",''))
                proxies.update(proxy)
        return proxies 
    def judge_proxies(self,proxy):
            proxies = {'http':'http://'+proxy}
            try:
                r = requests.get('http://tieba.baidu.com',proxies=proxies,headers=self.headers,timeout=2)
            except requests.exceptions.ConnectTimeout: 
                print(proxy+' ERROR')
            except :
                print('ERROR')
            else:
                self.proxies_list.append(proxy)
                print(proxy+' OK')
                
            
    def save_proxies(self):
        path = self.dir + 'proxies' 
        f = open(path,'w')
        for proxy in self.proxies_list:
            f.write(proxy+'\n') 
        f.close()

def main():
    urls = 'http://www.cybersyndrome.net/plr.html','http://www.proxylists.net','http://www.samair.ru/proxy/proxy-01.htm','http://proxylist.sakura.ne.jp'
    dir = '/home/emperor/Documents/'
    q = Queue()
    NUM = 50
    proxies = proxy(urls,dir) 
    jobs = proxies.spider()
    def mult_thread():
        while True:
            proxy = q.get()
            proxies.judge_proxies(proxy)
            q.task_done()
    for i in range(NUM):
        t = Thread(target=mult_thread)
        t.setDaemon(True) 
        t.start() 
    for p in jobs:
        q.put(p)
    q.join()
    proxies.save_proxies()
    

            
if __name__=='__main__':
    main()

        


