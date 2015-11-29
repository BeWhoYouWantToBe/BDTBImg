#!/usr/bin/env python
# coding=utf-8
import threading
import requests 
import queue
import time 
import os
from bs4 import BeautifulSoup 

queue = queue.Queue()
siteURL = 'http://www.dbmeinv.com/dbgroup/show.htm?cid={}&pager_offset={}'
dir = {'大胸妹':2,'美腿控':3,'有颜值':4,'大杂烩':5,'小翘臀':6,'黑丝袜':7}

class DBMV(threading.Thread):
    def __init__(self,queue,pdir):
        threading.Thread.__init__(self)
        self.pdir = pdir 

    def getPage(self,url):
        headers = {'Accept-Encoding':'gzip, deflate','Accept-Language':'zh-CN,en-US;q=0.7,en;q=0.3','Cache-Control':'max-age=0','Connection':'keep-alive','DNT':'1','Host':'www.dbmeinv.com',
                   'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0'}
        r = requests.get(url,headers) 
        soup = BeautifulSoup(r.text,'lxml')
        return soup 
    def getAllImg(self,soup):
        imgs = soup.find_all('img',class_='height_min') 
        srcs = {} 
        for img in imgs:
            srcs[img['title']] = img['src']
        return srcs 
    def saveImg(self,ImgURL,ImgName,path):
        data = requests.get(ImgURL).content 
        path = str(path) + ImgName
        f = open(path,'wb') 
        f.write(data)
        print('正在保存图片' + ImgName)
        f.close()
    def saveImgs(self,srcs,path):
        for name in srcs:
            ImgName = name 
            ImgURL = srcs[name] 
            self.saveImg(ImgURL,ImgName,path)
        time.sleep(1)
    def mkdir(self,path):
        path = path.strip() 
        isExists = os.path.exists(path) 
        if not isExists:
            os.makedirs(path) 
        return path

    def run(self):
        print('thread {} is running'.format(threading.current_thread().name))
        path = '/home/emperor/Pictures/dbmv/' + self.pdir + '/' 
        cateNum = dir[self.pdir]
        for i in range(1,5):
            url = siteURL.format(cateNum,i) 
            soup = self.getPage(url) 
            srcs = self.getAllImg(soup) 
            self.saveImgs(srcs,path)


def main():
    pdir = ['大胸妹','美腿控','有颜值','大杂烩','小翘臀','黑丝袜']
    for i in range(6):
        t = DBMV(queue,pdir[i])
        t.setDaemon(True)
        t.start()
        t.join()


if __name__ =='__main__':
    main()






        

        


    
