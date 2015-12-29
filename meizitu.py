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

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0'}


def get_proxy():
    return get_proxies.main()

all_proxies = get_proxy()

def get_urls():
    urls = {}
    for i in range(1, 3):
        tag = 1
        time.sleep(6)
        url = 'http://www.meizitu.com/a/list_1_{}.html'.format(i)
        while tag:
            wait = 10
            try:
                r = requests.get(url, timeout=8, headers=headers)
                tag = 0
            except:
                time.sleep(wait)
                wait += 5
        r.encoding = 'gb2312'
        soup = BeautifulSoup(r.text, 'lxml')
        div_tags = soup.find_all('div', {'class': 'pic'})
        for div in div_tags:
            urls[div.img['alt'].lstrip('<b>').rstrip('</b>')] = div.a['href']
        print('第{}页完成'.format(i))

    return urls


def mkdir(dirs):
    path = '/home/king/Pictures/meizitu/'
    for d in dirs:
        dir = path + d + '/'
        if not os.path.exists(dir):
            os.makedirs(dir)


def get_imgs(dir,url):
    dir = '/home/king/Pictures/meizitu/' + dir + '/'
    proxies = {}
    proxies['http'] = 'http://' + random.choice(all_proxies) 
    r = requests.get(url, timeout=8, headers=headers, proxies=proxies)
    r.encoding = 'gb2312'
    soup = BeautifulSoup(r.text, 'lxml')
    imgs = soup.find('div', {'id': 'picture'}).find_all('img')
    for i in imgs:
        path = dir + i['alt']
        save_img(path, i['src'])
        print(i['alt'] + ' 保存完成')
    time.sleep(6)


def save_img(full_path,pic_url):
    time.sleep(6)
    proxies = {}
    tag = 1
    while tag:
        try:
            r = requests.get(
                pic_url,
                timeout=10,
                headers=headers,
                proxies=proxies)
            tag = 0
        except:
            proxies = random.choice(all_proxies)
    f = open(full_path, 'wb')
    f.write(r.content)
    f.close()


def main():
    q = Queue()
    urls = get_urls()
    mkdir(urls.keys())
    def run():
        while 1:
            dir = q.get()
            get_imgs(dir,urls[dir])
            q.task_done()
    for i in range(10):
        t = Thread(target=run)
        t.setDaemon(True)
        t.start()
    for d in urls:
        q.put(d)
    q.join()


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
