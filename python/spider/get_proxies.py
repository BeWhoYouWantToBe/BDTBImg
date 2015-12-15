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
        self.dir = '/home/emperor/Documents/'
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
                r = requests.get('http://tieba.baidu.com',proxies=proxies,headers=self.headers,timeout=8)
            except requests.exceptions.ConnectTimeout: 
                print(proxy+'Timeout')
            except :
                print('ERROR')
            else:
                if '全球最大的中文社区' in r.text:
                    self.proxies_list.append(proxy)
                    print(proxy+' OK')

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
    pdb.set_trace()
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
    proxies.save_proxies()
    
            
if __name__=='__main__':
    main()

        


