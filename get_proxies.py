#!/usr/bin/env python
# coding=utf-8 
import gevent.monkey
gevent.monkey.patch_socket()

import gevent 
import requests 
#from queue import Queue 
from gevent.queue import Queue
#from threading import Thread
from bs4 import BeautifulSoup  

class proxy():
    def __init__(self):
        self.urls = ['http://www.kuaidaili.com/free/','http://www.kxdaili.com/dailiip/','http://www.xicidaili.com/','http://ip84.com/gn/','http://www.nianshao.me/?page=','http://www.swei360.com/free/?stype={}&page=','http://www.004388.com/','http://www.bigdaili.com/dailiip/','http://www.mayidaili.com/free/anonymous/高匿/']
        self.dir = '/home/king/Documents/'
        self.proxies_list = []
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

    def get_proxies(self):
        proxies = set() 
        for url in self.urls:
            if url == self.urls[0] or url == self.urls[1] or url == self.urls[2] or url == self.urls[5] or url == self.urls[7]:
                for i in range(1,7):
                    if url == self.urls[0]:
                        inpurl = url + 'inha/' + str(i)
                        outpurl = url + 'outha/' + str(i)
                        j = 0
                    elif url == self.urls[1] or url == self.urls[7]:
                        inpurl = url + '1/'  + '{}.html#ip'.format(i)
                        outpurl = url + '3/' + '{}.html#ip'.format(i)
                        j = 1
                    elif url == self.urls[2]:
                        inpurl = url + 'nn/' + str(i)
                        outpurl = url + 'wn/' + str(i)
                        j = 2
                    elif url == self.urls[5]:
                        inpurl = url.format(1) + str(i) 
                        outpurl = url.format(3) + str(i)
                        j = 5
                    try:
                        inr = requests.get(inpurl,headers=self.headers)
                    except:
                        break
                    outr = requests.get(outpurl,headers=self.headers)
                    insoup = BeautifulSoup(inr.text,'lxml')
                    outsoup = BeautifulSoup(outr.text,'lxml')
                    try:
                        trs = insoup.find_all('tr')[1:] 
                    except:
                        print('抓取代理失败')
                    try:
                        outtrs = outsoup.find_all('tr')[1:]
                    except:
                        print('抓取代理失败')
                    else:
                        trs.extend(outtrs) 
                    if j == 2:
                        for tr in trs:
                            proxy = tr.contents[5].string + ':' +  tr.contents[7].string 
                            proxies.add(proxy)
                    else:
                        for tr in trs:
                            proxy = tr.contents[1].string + ':' + tr.contents[7].string
                            proxies.add(proxy)
            elif url == self.urls[3] or url ==self.urls[4]:
                for i in range(1,7):
                    url = url + str(i)
                    try:
                        r = requests.get(url,headers=self.headers)
                    except:
                        break
                    soup = BeautifulSoup(r.text,'lxml')
                    try:
                        trs = soup.find_all('tr')[1:]
                    except:
                        print('抓取代理失败')
                    else:
                        for tr in trs:
                            proxy = tr.contents[1].string + ':' + tr.contents[7].string 
                            proxies.add(proxy) 
            elif url == self.urls[6]:
                for i in range(1,7):
                    inpurl = url + 'ip/index_{}.html'.format(i)
                    outpurl = url + 'ipgw/index_{}.html'.format(i) 
                    try:    
                        inr = requests.get(inpurl,headers=self.headers)
                        outr = requests.get(outpurl,headers=self.headers)
                    except:
                        break
                    insoup = BeautifulSoup(inr.text,'lxml')
                    outsoup = BeautifulSoup(outr.text,'lxml')
                    try:
                        trs = insoup.find_all('tr')[7:-2] 
                    except:
                        print('抓取代理失败')
                    try:
                        outtrs = outsoup.find_all('tr')[7:-2]
                    except:
                        print('抓取代理失败')
                    else:
                        trs.extend(outtrs) 
                        for tr in trs:
                            proxy = tr.contents[3].string + ':' + tr.contents[5].string
                            proxies.add(proxy)
            elif url == self.urls[8]:
                '''               
                for i in range(50):
                    url = url + str(i)
                    try:
                        r = requests.get(url,headers=self.headers)
                    except:
                        break
                    soup = BeautifulSoup(r.text,'lxml')
                    try:
                        trs = soup.find_all('tr')[1:]
                    except:
                        print('抓取代理失败')
                    for tr in trs:
                        proxy = tr.contents[1].string + ':' + tr.contents[3].span.string 
                        proxies.add(proxy) 
                '''

                q = Queue()
                NUM = 40 
                jobs = [url + str(i) for i in range(200)]
                def worker():
                    while not q.empty():
                        url = q.get() 
                        try:
                            r = requests.get(url,headers=self.headers) 
                        except:
                            pass 
                        soup = BeautifulSoup(r.text,'lxml')
                        try:
                            trs = soup.find_all('tr')[1:] 
                        except:
                            print('抓取代理失败')
                        else:
                            for tr in trs:
                                proxy = tr.contents[1].string + ':' + tr.contents[3].span.string 
                                proxies.add(proxy)
                        gevent.sleep(0)

                def boss():
                    for job in jobs:
                        q.put_nowait(job)

                gevent.spawn(boss).join() 
                threads = [gevent.spawn(worker) for i in range(NUM)]
                gevent.joinall(threads)



        return proxies 

    def judge_proxies(self,proxy):
            proxies = {'http':'http://'+proxy}
            try:
                r = requests.get('http://www.icanhazip.com',proxies=proxies,headers=self.headers,timeout=6)
            except requests.exceptions.ConnectTimeout:
                print(proxy+' Timeout')
            except:
                print("ERROR")
            else:
                if r.text.strip() == proxy.split(':')[0]:
                    try:
                        r = requests.get('http://mp.weixin.qq.com/s?__biz=MzA4MjYwODg0OQ==&mid=400800258&idx=1&sn=deb6bd1efcfc5ba2a3fcd422c3a54e75&3rd=MzA3MDU4NTYzMw==&scene=6#rd',proxies=proxies,headers=self.headers,timeout=6)
                    except requests.exceptions.ConnectTimeout:
                        print(proxy+' Timeout')
                    except:
                        print('ERROR')
                    else:
                        if len(r.text) == 30945:
                            self.proxies_list.append(proxy)
                            print(proxy+' OK')

    def save_proxies(self):
        path = self.dir + 'proxies' 
        f = open(path,'w')
        for proxy in self.proxies_list:
            f.write(proxy+'\n') 
        f.close()

def main():
#    q = Queue()
#   NUM = 60
#    proxies = proxy() 
#    jobs = proxies.get_proxies()
#    def mult_thread():
#        while True:
#            proxy = q.get()
#            proxies.judge_proxies(proxy)
#            q.task_done()
#    for i in range(NUM):
#        t = Thread(target=mult_thread)
#        t.setDaemon(True) 
#        t.start() 
#    for p in jobs:
#        q.put(p)
#    q.join()
#    if __name__=='__main__':
#        proxies.save_proxies()
#    else:
#        return proxies.proxies_list
    q = Queue()
    NUM = 60
    proxies = proxy()   
    jobs = proxies.get_proxies()

    def worker():
        while not q.empty():
            job = q.get() 
            proxies.judge_proxies(job)
            gevent.sleep(0)

    def boss():
        for job in jobs:
            q.put_nowait(job)

    gevent.spawn(boss).join() 

    threads = [gevent.spawn(worker) for i in range(NUM)]
    gevent.joinall(threads)
    print('共获得{}个代理'.format(len(proxies.proxies_list)))

    if __name__ == '__main__':
        proxies.save_proxies() 
    else:
        return proxies.proxies_list 


            
            

    
if __name__=='__main__':
    main()

        


