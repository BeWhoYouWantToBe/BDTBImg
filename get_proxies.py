#!/usr/bin/env python
# coding=utf-8
import pdb
import requests 
from queue import Queue
from threading import Thread
from bs4 import BeautifulSoup 

class proxy():
    def __init__(self):
        self.urls = ['http://www.kuaidaili.com/proxylist/','http://www.kxdaili.com/ipList/{}.html#ip']
        self.dir = '/home/king/Documents/'
        self.proxies_list = []
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

    def get_proxies(self):
        proxies = set() 
        for url in self.urls:
            if url == self.urls[0] or url == self.urls[1]:
                for i in range(1,11):
                    if url == self.urls[0]:
                        purl = url + str(i)
                    else:
                        purl = url.format(i)
                    r = requests.get(purl,headers=self.headers)
                    soup = BeautifulSoup(r.text,'lxml')
                    try:
                        trs = soup.find_all('tr')[1:] 
                    except:
                        print('抓取代理失败')
                    else:
                        for tr in trs:
                            proxy = tr.contents[1].string + ':' +  tr.contents[3].string
                            proxies.add(proxy)
        return proxies 

    def judge_proxies(self,proxy):
            proxies = {'http':'http://'+proxy}
            try:
                r = requests.get('http://www.meizitu.com/a/5217.html',proxies=proxies,headers=self.headers,timeout=3)
            except requests.exceptions.ConnectTimeout: 
                print(proxy+'Timeout')
            except :
                print('ERROR')
            else:
                if len(r.text)== 17399 :
                    self.proxies_list.append(proxy)
                    print(proxy+' OK')
                else:
                    print('ERROR')

    def save_proxies(self):
        path = self.dir + 'proxies' 
        f = open(path,'w')
        for proxy in self.proxies_list:
            f.write(proxy+'\n') 
        f.close()

def main():
    q = Queue()
    NUM = 30
    proxies = proxy() 
    jobs = proxies.get_proxies()
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
    if __name__=='__main__':
        proxies.save_proxies()
    else:
        return proxies.proxies_list


if __name__=='__main__':
    main()

        


