import urllib.parse
from bs4 import BeautifulSoup
import requests
import re
import time 

def download_lyrics(song_url):
    # downloading lyrics file 
    musicPlayPage = requests.session().get(url=song_url)
    if musicPlayPage.status_code == 200:
        musicPlayContent = musicPlayPage.content 
        soup = BeautifulSoup(musicPlayContent, 'html.parser')
        lyricUrlDiv = soup.find_all('div', attrs={'id':'lyricCont'})
        lyricUrl = re.findall('data-lrclink="(.*?)" id="lyricCont">',str(lyricUrlDiv[0]))

        lyricPage = requests.session().get(url=lyricUrl[0])
        if lyricPage.status_code ==200:
            nameDiv = soup.find_all('h2', attrs={'class':'songpage-title clearfix'})
            name = re.findall('<h2 class="songpage-title clearfix" title="(.*?)">', str(nameDiv[0]))
            playFile = open('./lyricsDir/'+name[0], 'wb')
            
            for chunk in lyricPage.iter_content(100000):
                playFile.write(chunk)
            playFile.close()

            time.sleep(2)


def spider():
    song_labels = ['新歌', '热歌', '中国好声音','经典老歌','电视剧','80后','网络歌曲','儿歌','粤语','民歌','对唱']
    for songLabel in song_labels:
        indexPageUrl ='http://music.taihe.com/tag/'+str(urllib.parse.quote(songLabel))
        for start in range(50):
            startIndex = start*20
            third_type = 0
            pageUrl = indexPageUrl +'?start='+str(startIndex)+'&size=20'+'&third_type=0'
            musicIndexPage = requests.session().get(url=pageUrl)

            if musicIndexPage.status_code ==200:
                
                musicIndexContent = musicIndexPage.content 
                soup = BeautifulSoup(musicIndexContent, 'html.parser')
                musicLis = soup.find_all('span', attrs={'class':'song-title'})

                for musicLi in musicLis:
                    result_replace = str(musicLi).replace('\r\n\t','<br/>').replace('\n\t','<br/>').replace('\n','<br/>')
                    song_url_name = re.findall('href="(.*?)" target="_blank" title=".*?">(.*?)</a><div class="extra-info">',result_replace)[0]
                    song_url = 'http://music.taihe.com/'+song_url_name[0]
                    download_lyrics(song_url)
                    

def main():
    spider()

if __name__ == "__main__":
    main()


