#!/usr/bin/env python
# coding=utf-8
import requests 
import os
import optparse 
import queue 
import re
from bs4 import BeautifulSoup 

pattern1 = re.compile(r'/p/\d+\?pn=\d')
pattern2 = re.compile(r'/f\?kw=\w+&ie=utf-8&pn=\d+')

def extract_urls(current_url):
    r = requests.get(current_url)
    soup = BeautifulSoup(r.text,'lxml')
    pageList = soup.find_all('a',href='pattern1') 
    urls = set() 
    for a in pageList:
        urls.add('http://tieba.baidu.com' + a['href'])
    return urls

def getTBNP(current_url):
    r = requests.get(current_url) 
    soup = BeautifulSoup(r.text,'lxml') 
    pageList = soup.find_all('a',href=pattern2)
    urls = set() 
    for a in pageList:
        urls.add('http://tieba.baidu.com' + a['href'])
    return urls
    


def imgDown(url,dir):
    init_page = url;
    url_queue = queue.Queue() 
    seen = set()
    seen.add(init_page) 
    url_queue.put(init_page)
    i = 0

    while(True):
        if url_queue.qsize() > 0:
            current_url = url_queue.get()
            r = requests.get(current_url)
            soup = BeautifulSoup(r.text,'lxml')
            img_tag = soup.find_all('img',class_='BDE_Image')
            for img in img_tag:
                imgname = img['src'].lstrip('http://')
                imgname = os.path.join(dir,imgname.replace('/','_'))
                i += 1
                print('[+] Saving'  + '第{}张图片'.format(i))
                pic = requests.get(img['src']).content
                save = open(imgname,'wb')
                save.write(pic)
                save.close()
            urls = extract_urls(current_url)
            for next_url in urls: 
                if next_url not in seen:
                    seen.add(next_url) 
                    url_queue.put(next_url)

        else:
            break

def BDTB(name,dir):
    i = 0
    TZURL_queue = queue.Queue()
    seen_TZ = set() 
    url = 'http://tieba.baidu.com/f?kw=' + name + '&ie=utf-8&pn=0' 
    seen_TZ.add(url)
    TZURL_queue.put(url)
    while True:
        if TZURL_queue.qsize() > 0:
            i += 1
            current_url = TZURL_queue.get()
            r = requests.get(current_url)
            soup = BeautifulSoup(r.text,'lxml') 
            print('正在下载第{}页帖子的图片'.format(i))
            TZUrls = soup.find_all('a',class_='j_th_tit')    #注意缩进 一旦错误会造成非常恶心第逻辑问题
            for  TZUrl in TZUrls:
                url = 'http://tieba.baidu.com' + TZUrl['href']
                imgDown(url,dir)
            TZURLS = getTBNP(current_url) 
            for next_url in TZURLS:
                if next_url not in seen_TZ:
                    seen_TZ.add(next_url) 
                    TZURL_queue.put(next_url)
        else:
            break





def main():
    parser = optparse.OptionParser('usage%prog -n <target TBName> -d <destination directory>')
    parser.add_option('-n',dest='name',type='string',help='specify target TBName')
    parser.add_option('-d',dest='dir',type='string',help='specify destination directory')
    options,args = parser.parse_args()
    name  = options.name
    dir = options.dir
    if name == None or dir == None:
        print(parser.usage)
        exit(0)
    else:
        try:
            BDTB(name,dir) 
        except Exception as e:
            print('[-] Error BDTB')
            print(e)

if __name__ == '__main__':
    main()

    







