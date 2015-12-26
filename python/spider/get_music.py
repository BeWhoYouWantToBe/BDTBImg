#!/usr/bin/env python
# coding=utf-8
import re 
import pdb
import json
import optparse
import requests 
import urllib.parse
from bs4 import BeautifulSoup 

class Music():
    def __init__(self,pdir,name):
        self.pdir = pdir
        self.name = name 
        self.search_url = ('http://music.163.com/#/search/m/?s=','http://www.xiami.com/search?key=') 
        self.info_url = ('http://music.163.com/api/song/detail/?id=song_num&ids=["song_num"]','http://www.xiami.com/song/playlist/id/')
        self.headers = {  
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'  
    }  
    def get_song_num(self):
        i = 0
        n = len(self.search_url)
        tag = ('b','a')
        while(i<n):
            try:
                search_url = self.search_url[i] + self.name 
            except:
                print('网易云音乐和虾米音乐都没有该歌曲')
                exit(0)
            else:
                 
                if i == 0:
                    headers = self.headers
                    headers['Referer'] = 'http://music.163.com'
                    r = requests.get(search_url,headers=headers) 
                    soup = BeautifulSoup(r.text,'lxml') 
                    a = soup.find(tag[i],title=self.name)
                    href = a.parent['href']
                    song_num = href.split('=')[-1]
                    return song_num,i 
                elif i == 1:
                    r = requests.get(search_url,headers=headers) 
                    soup = BeautifulSoup(r.text,'lxml') 
                    a = soup.find(tag[i],title=self.name)   
                    song_num = a['href'].split('/')[-1] 
                    return song_num,i 
                
                else:
                    i += 1
            
    def get_down_url(self,song_num_i):
        if song_num_i[1] == 0:
            info_url = self.info_url[0].replace('song_num',song_num_i[0])
            r = requests.get(info_url,headers=self.headers)
            data = json.load(r.text)
            url = data['songs'][0]['mp3Url'] 
            return url
        elif song_num_i[1] == 1:
            info_url = self.info_url[1] + song_num_i[0]
            r = requests.get(info_url,headers=self.headers)
            soup = BeautifulSoup(r.text,'lxml')
            try:
                location =  soup.find('location').string 
            except AttributeError :
                print('歌曲没有版权')
            except:
                print('Error')
            else:
                return self.decrypt(location)
    def decrypt(self,location):
        strlen = len(location[1:])  
        rows = int(location[0])  
        cols = strlen // rows  
        right_rows = strlen % rows  
        new_str = location[1:]   
        true_url = ''  
        for i in range(strlen):  
            x = i % rows  
            y = i / rows  
            p = 0  
            if x <= right_rows:  
                p = x * (cols + 1) + y  
            else:  
                p = right_rows * (cols + 1) + (x - right_rows) * cols + y  
            true_url += new_str[int(p)]  
        url = urllib.parse.unquote(true_url).replace('^','0')
        return url
    def save_music(self,down_url):
        path = self.pdir + self.name 
        data = requests.get(down_url,headers=self.headers).content
        f = open(path,'wb') 
        f.write(data)
        f.close()
        print('歌曲'+self.name+'保存完成')
        
        


def main():
    parser = optparse.OptionParser('usage%prog -n <target name>') 
    parser.add_option('-n',dest='name',type='string',help='specify music name')
    options,args = parser.parse_args()
    name = options.name
    if name == None:
        print(parser.usage)
        exit(0)
    music = Music('/home/emperor/',name)
    pdb.set_trace()
    song_num_i = music.get_song_num()
    down_url = music.get_down_url(song_num_i)
    music.save_music(down_url)



if __name__ == '__main__':
    main()


