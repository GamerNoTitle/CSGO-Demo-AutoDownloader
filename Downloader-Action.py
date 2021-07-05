import json as js
import time
import re
import requests as r
from http.cookies import SimpleCookie
import os
import sys

WelcomeMsg='''======================== Counter-Strike: Global Offensive Demo Downloader ========================
Thanks for your using on CSGO-Demo-AutoDownloader, This is a automatic downloader that helps you download your newest CSGO demos
The project is maintained by GamerNoTitle. If this project helps you, consider donate please.

Paypal: https://paypal.me/GamerNoTitle
afdian: https://afdian.net/@GamerNoTitle
Alipay (QR Code): https://cdn.jsdelivr.net/gh/GamerNoTitle/Picture-repo-v1@master/img/Payments/AliPay.jpg
WechatPay (QR Code): https://cdn.jsdelivr.net/gh/GamerNoTitle/Picture-repo-v1@master/img/Payments/WeChat.png
==================================================================================================
'''

print(WelcomeMsg)

sessionid,steamid64,steamcustomid,cookie,previousdownload = sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5]
cookieSimple = SimpleCookie(cookie)
cookieDecoded = {i.key:i.value for i in cookieSimple.values()}
continuetoken=0
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja-JP;q=0.6,ja;q=0.5',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': cookie,
    'DNT': '1',
    'Host': 'steamcommunity.com',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

if steamcustomid == '' and int(steamid64) != 0 and steamid64 != '':
    CompetitionStatsLink = "https://steamcommunity.com/profile/{}/gcpd/730?ajax=1&tab=matchhistorycompetitive".format(steamid64)
elif steamcustomid != '':
    CompetitionStatsLink = "https://steamcommunity.com/id/{}/gcpd/730?ajax=1&tab=matchhistorycompetitive".format(steamcustomid)
else:  
    CompetitionStatsLink = False

def progressbar(url,path):
    start = time.time() 
    response = r.get(url, stream=True) 
    size = 0    
    chunk_size = 1024  
    content_size = int(response.headers['content-length'])  
    try:
        if response.status_code == 200:   
            print('[INFO]Start download, File size:{size:.2f} MB'.format(size = content_size / chunk_size /1024))   
            filepath = path  
            with open(filepath,'wb') as file:   
                for data in response.iter_content(chunk_size = chunk_size):
                    file.write(data)
                    size +=len(data)
                    print('\r'+'[INFO]Downloading: %s%.2f%%' % ('>'*int(size*50/ content_size), float(size / content_size * 100)) ,end=' ')
        end = time.time()
        print('[INFO]Download completed! Times: %.2f seconds' % (end - start))
    except:
        print('[INFO]Download failed.')

def Download():
    if not CompetitionStatsLink:
        print('[ERROR]Neither steamid64 nor steamcustomid has been set. The program will exit now.')
        sys.exit()
    CompetitionList = r.get(CompetitionStatsLink, headers=headers).text
    while True:
        LinkList=[]
        LinkList = re.findall(r'"http:\\\/\\\/replay141.valve.net\\\/730\\\/................................\.dem\.bz2', CompetitionList)
        if LinkList == []:
            print('[INFO]There\'s no any demo to download, download process accomplished. The program will now exit.')
            break
        try:
            continuetoken = str(re.findall(r'\"continue_token\"\:\"[0-9]+\"', CompetitionList)[0]).replace('"','').replace('continue_token:','')
            print('[INFO]New continue token has been set. If you enabled previous download mode, this token will work.')
        except:
            print('[WARN]continue token not found. Don\'t worry, we will use the previous one.')
        for link in LinkList:
            filelink=link
            filename=link[40:]
            if os.path.exists('./Demo/'+filename):
                print('[INFO]Demo file {} exists, skipping download process.'.format(filename))
            else:
                print('[INFO]Downloading {} from {}'.format(filename,filelink.replace('\\','').replace('"','')))
                progressbar(filelink.replace('\\','').replace('"',''),'./Demo/'+filename)
                # with open('./Demo/'+filename,'wb+') as f:
                #     f.write(r.get(filelink.replace('\\','').replace('"','')).content)
                #     f.close
        if previousdownload == 'true' or previousdownload == 'True':
            print('[INFO]Previous download mode is enabled. Download process will continue.')
            CompetitionList = r.get(CompetitionStatsLink+'&continue_token={}&sessionid={}'.format(continuetoken,sessionid),headers=headers).text
        else:
            print('[INFO]Previous download mode is disabled. The program will now exit.')
            break

if __name__ == '__main__':
    Download()