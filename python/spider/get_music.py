#!/usr/bin/env python
# coding=utf-8
import re
import requests 
import urllib.parse
from bs4 import BeautifulSoup 

class Music():
    def __init__(self,pdir,name):
        self.pdir = pdir
        self.name = name
        self.headers = {  
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'  
    }  
    def get_song_num(self):
        search_url = 'http://www.xiami.com/search?key=' + self.name 
        r = requests.get(search_url,headers=self.headers) 
        soup = BeautifulSoup(r.text,'lxml') 
        a = soup.find('a',title=self.name) 
        song_num = a['href'].split('/')[-1] 
        return song_num 
    def get_song_location(self,song_num):
        xml_info_url = 'http://www.xiami.com/song/playlist/id/' + song_num 
        r = requests.get(xml_info_url,headers=self.headers) 
        soup = BeautifulSoup(r.text,'lxml') 
        location =  soup.find('location').string 
        return location
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
        return urllib.parse.unquote(true_url).replace('^','0')
    def save_music(self,down_url):
        path = self.pdir + self.name 
        data = requests.get(down_url,headers=self.headers).content
        f = open(path,'wb') 
        f.write(data)
        f.close()
        print('歌曲'+self.name+'保存完成')
        
        


def main():
    music = Music('/home/emperor/','花甲')
    song_num = music.get_song_num()
    location = music.get_song_location(song_num) 
    down_url = music.decrypt(location) 
    music.save_music(down_url)



if __name__ == '__main__':
    main()


