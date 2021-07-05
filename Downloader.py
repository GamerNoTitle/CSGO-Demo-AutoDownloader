import json as js
import time
import re
import requests as r
from http.cookies import SimpleCookie

with open('./config.json','r') as f:
    config=js.load(f)
    f.close()

steamcustomid = config['steamcustomid']
steamid64 = config['steamid64']
proxies = config['proxies']
cookie = config['steamcookie']
cookieSimple = SimpleCookie(cookie)
cookieDecoded = {i.key:i.value for i in cookieSimple.values()}
sessionid=cookieDecoded['sessionid']
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

if steamcustomid == '' and steamid64 != 0:
    CompetitionStatsLink = "https://steamcommunity.com/profile/{}/gcpd/730?ajax=1&tab=matchhistorycompetitive&sessionid={}".format(steamid64,sessionid)
elif steamcustomid != '':
    CompetitionStatsLink = "https://steamcommunity.com/id/{}/gcpd/730?ajax=1&tab=matchhistorycompetitive&sessionid={}".format(steamcustomid,sessionid)

if __name__ == '__main__':
    if(proxies['http']=='' and proxies['https']==''):
        CompetitionList = r.get(CompetitionStatsLink, headers=headers).text
    else:
        CompetitionList = r.get(CompetitionStatsLink, proxies=proxies, headers=headers).text
    LinkList = re.findall(r'"http:\\\/\\\/replay141.valve.net\\\/730\\\/................................\.dem\.bz2', CompetitionList)
    for link in LinkList:
        filelink=link
        filename=link[40:]
        print('[INFO]Downloading {}'.format(filelink.replace('\\','')))
        with open('./Demo/'+filename,'wb+') as f:
            f.write(r.get(filelink.replace('\\','').replace('"','')).content)
            f.close