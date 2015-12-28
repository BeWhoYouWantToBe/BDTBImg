#!/usr/bin/env python
# coding=utf-8
import os 
import pdb
import time
import gevent 
import requests
from bs4 import BeautifulSoup 

headers = {'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0'}

def get_urls():
    urls = {}
    for i in range(1,3):
        tag = 1
        time.sleep(5)
        url = 'http://www.meizitu.com/a/list_1_{}.html'.format(i)
        while tag:
            wait = 10
            try:
                r = requests.get(url,timeout=5,headers=headers)
                tag = 0
            except:
                time.sleep(wait) 
                wait += 5
        r.encoding = 'gb2312'
        soup = BeautifulSoup(r.text,'lxml') 
        div_tags = soup.find_all('div',{'class':'pic'})
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
    dir = '/home/king/Pictures/meizitu/' + dir +'/'
    r = requests.get(url,timeout=5,headers=headers) 
    r.encoding = 'gb2312'
    soup = BeautifulSoup(r.text,'lxml') 
    imgs = soup.find('div',{'id':'picture'}).find_all('img')
    for i in imgs:
        path = dir + i['alt']
        save_img(path,i['src'])
        print(i['alt']+' 保存完成')

def save_img(full_path,pic_url):
    r = requests.get(pic_url,timeout=10,headers=headers)
    f = open(full_path,'wb') 
    f.write(r.content)
    f.close()
    

def main():
    urls = get_urls()
    mkdir(urls.keys())
    for dir in urls:
        get_imgs(dir,urls[dir])
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

if __name__=='__main__':
    main()


