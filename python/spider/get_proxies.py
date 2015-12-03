#!/usr/bin/env python
# coding=utf-8
import re 
import pdb
import requests
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
    def spider(self):
        proxies = set() 
        for url in self.urls:
            r = requests.get(url) 
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
            #elif url == self.urls[2]:
            #    proxy = soup.find_all() 
            #    proxies.updata(proxy)    待完善
            else:
                args = soup.find_all(text=re.compile(r'\(\d\,'))
                proxy = []
                for arg in args:
                    proxy.append(get_sakura_ne_jp(arg.lstrip("\\n<!--\nproxy(").rstrip(');\n// -->\n').split(',')).replace("'",''))
                proxies.update(proxy)
        return proxies 
    def judge_proxies(self):
        Proxies = self.spider()
        proxies_list = []
        for proxy in Proxies:
            proxies = {'http':'http://'+proxy}
            try:
                r = requests.get('http://tieba.baidu.com',proxies=proxies,timeout=2)
            except requests.exceptions.ConnectTimeout: 
                print(proxy+' ERROR')
            except :
                print('ERROR')
            else:
                proxies_list.append(proxy)
                print(proxy+' OK')
        return proxies_list
                
            
    def save_proxies(self):
        proxies = self.judge_proxies()
        path = self.dir + 'proxies' 
        f = open(path,'w')
        for proxy in proxies:
            f.write(proxy+'\n') 
        f.close()

def main():
    urls = 'http://www.cybersyndrome.net/plr.html','http://www.proxylists.net','http://www.samair.ru/proxy/proxy-01.htm','http://proxylist.sakura.ne.jp'
    dir = '/home/emperor/Documents/'
    proxies = proxy(urls,dir) 
    proxies.save_proxies()

if __name__=='__main__':
    main()

        


