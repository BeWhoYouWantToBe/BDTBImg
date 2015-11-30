#!/usr/bin/env python
# coding=utf-8
import re 
import pdb
import socket
import requests
from bs4 import BeautifulSoup

class proxy():
    def __init__(self,url,dir):
        self.url = url 
        self.dir = dir 
    def spider(self):
        r = requests.get(self.url) 
        soup = BeautifulSoup(r.text,'lxml') 
        proxies = soup.find_all('td',text=re.compile(':'))
        return proxies 
    def judge_proxies(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        Proxies = self.spider()
        proxies_list = []
        for proxy in Proxies:
            try:
                s.connect(proxy.text.split(':')[0],int(proxy.text.split(';')[1]))
                s.close()
                proxies_list.append(proxy)
            except:
                pass 
        return proxies_list
                
            
    def save_proxies(self):
        proxies = self.judge_proxies()
        path = self.dir + 'proxies' 
        f = open(path,'w')
        for proxy in proxies:
            f.write(proxy.text+'\n') 
        f.close()

def main():
    url = 'http://www.cybersyndrome.net/plr.html'
    dir = '/home/emperor/Documents/'
    proxies = proxy(url,dir) 
    pdb.set_trace()
    proxies.save_proxies()

if __name__=='__main__':
    main()

        


