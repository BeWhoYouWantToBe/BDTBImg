#!/usr/bin/env python
# coding=utf-8
import os
import pdb
import time 
import requests
import random
import get_proxies
from bs4 import BeautifulSoup
from threading import Thread
from queue import Queue  

Headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Encoding':'gzip, deflate','Accept-Language':'zh-CN,en-US;q=0.7,en;q=0.3','DNT':'1','Host':'www.meizitu.com','Referer':'http://www.meizitu.com/','User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0'}

headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0','Accept':'image/png,image/*;q=0.8,*/*;q=0.5','AcceptEncoding':'gzip,deflate','Accept-Language':'zh-CN,en-US;q=0.7,en;q=0.3','Cache-Control':'max-age=0','DNT':'1','Referer':'http://www.meizitu.com/'}


def get_proxy():
    return get_proxies.main()

all_proxies = get_proxy()

def get_urls():
    urls = {}
    for i in range(9,11):
        tag = 1
        time.sleep(3)
        url = 'http://www.meizitu.com/a/list_1_{}.html'.format(i)
        wait = 10
        while tag:
            try:
                r = requests.get(url, timeout=10, headers=Headers)
                tag = 0
            except:
                time.sleep(wait)
                wait += 5
        r.encoding = 'gb2312'
        soup = BeautifulSoup(r.text, 'lxml')
        div_tags = soup.find_all('div', {'class': 'pic'})
        for div in div_tags:
            urls[div.img['alt'].lstrip('<b>').rstrip('</b>')] = div.a['href']
        print('第{}页提取完成'.format(i))

    return urls


def mkdir(dirs):
    path = '/home/king/Pictures/meizitu/'
    for d in dirs:
        dir = path + d + '/'
        if not os.path.exists(dir):
            os.makedirs(dir)


def get_imgs(dir,url,proxy):
    proxies = {}
    proxies['http'] = 'http://' + proxy
    dir = '/home/king/Pictures/meizitu/' + dir + '/'
    Tag = 1
    while Tag:
        try:
            r = requests.get(url, timeout=10, headers=Headers,proxies=proxies)
            Tag = 0
        except:
            proxies['http'] = 'http://' + random.choice(all_proxies[5:-1])
    r.encoding = 'gb2312'
    soup = BeautifulSoup(r.text, 'lxml')
    imgs = soup.find('div', {'id': 'picture'}).find_all('img')
    for i in imgs:
        path = dir + i['alt']
        save_img(path, i['src'],proxies)
        print(i['alt'] + ' 保存完成')
    time.sleep(3)


def save_img(full_path,pic_url,proxies):
    time.sleep(3)
    tag = 1
    wait = 10
    while tag:
        try:
            r = requests.get(pic_url,timeout=3,headers=headers,proxies=proxies)
            tag = 0
        except:
            time.sleep(wait)
            wait += 5
    f = open(full_path, 'wb')
    f.write(r.content)
    f.close()


def main():
    q = Queue()
    urls = get_urls()
    mkdir(urls.keys())
    def run(proxy):
        while 1:
            dir = q.get()
            get_imgs(dir,urls[dir],proxy)
            q.task_done()
    for i in range(5):
        proxy = all_proxies[i]
        for j in range(6):
            t = Thread(target=run,args=(proxy,))
            t.setDaemon(True)
            t.start()
    for d in urls:
        q.put(d)
    q.join()
    print('全部下载完成')


#    tasks = []
#    while urls:
#        dirs = []
#        i = 0
#        for dir in urls:
#            if i<10:
#                tasks.append(gevent.spawn(get_imgs,dir,urls[dir]))
#                dirs.append(dir)
#                i += 1
#            else:
#                break
#        for dir in dirs:
#            del urls[dir]
#        gevent.joinall(tasks)

if __name__ == '__main__':
    main()
