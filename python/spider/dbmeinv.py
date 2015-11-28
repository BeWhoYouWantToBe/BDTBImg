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
class DBMV(threading.Thread):
    def __init__(self,queue,pdir):
        threading.Thread.__init__(self)
        self.queue = queue
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
        while True:
            path = '/home/emperor/Pictures/dbmv/' + self.pdir + '/' 
            url = self.queue.get() 
            soup = self.getPage(url) 
            srcs = self.getAllImg(soup) 
            print('thread {} is running'.format(threading.current_thread().name))
            self.saveImgs(srcs,path)
            self.queue.task_done()


def main():
    dir = ['大胸妹','美腿控','有颜值','大杂烩','小翘臀','黑丝袜']
    for i in range(6):
        t = DBMV(queue,dir[i])
        t.setDaemon(True)
        t.start()

    for i in range(2,8):    #逻辑错误 
        url = siteURL.format(i,4) 
        queue.put(url)

    queue.join()

if __name__ =='__main__':
    main()






        

        


    
