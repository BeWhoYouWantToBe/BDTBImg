#!/usr/bin/env python
# coding=utf-8
import requests 
import os
import optparse 
import queue
from bs4 import BeautifulSoup 

def extract_urls(current_url):
    r = requests.get(current_url)
    soup = BeautifulSoup(r.text,'lxml')
    li = soup.find('li',class_='l_pager pager_theme_4 pb_list_pager')
    span = li.span
    urls = []
    for a in span.next_siblings: 
        if(str(type(a)) == "<class 'bs4.element.Tag'>"):
            urls.append('http://tieba.baidu.com' + str(a['href']))
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

def main():
    parser = optparse.OptionParser('usage%prog -u <target url> -d <destination directory>')
    parser.add_option('-u',dest='url',type='string',help='specify target url')
    parser.add_option('-d',dest='dir',type='string',help='specify destination directory')
    options,args = parser.parse_args()
    url = options.url
    dir = options.dir
    if url == None or dir == None:
        print(parser.usage)
        exit(0)
    else:
        try:
            imgDown(url,dir)
        except Exception as e:
            print('[-] Error imgDown')
            print(e)

if __name__ == '__main__':
    main()

    







