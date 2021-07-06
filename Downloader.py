import json as js
import time
import re
import requests as r
from http.cookies import SimpleCookie
import os
import sys

with open('./config.json','r') as f:
    config=js.load(f)
    f.close()

lang = config['lang']
steamcustomid = config['steamcustomid']
steamid64 = config['steamid64']
proxies = config['proxies']
cookie = config['steamcookie']
cookieSimple = SimpleCookie(cookie)
cookieDecoded = {i.key:i.value for i in cookieSimple.values()}
sessionid=cookieDecoded['sessionid']
previousdownload=config['previousdownload']
continuetoken=0
delay=config['delay']
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

with open('./i18n/{}.json'.format(lang),'r') as langfile:
    LangDict = js.load(langfile)
    langfile.close()

if steamcustomid == '' and steamid64 != 0:
    CompetitionStatsLink = "https://steamcommunity.com/profile/{}/gcpd/730?ajax=1&tab=matchhistorycompetitive".format(steamid64)
elif steamcustomid != '':
    CompetitionStatsLink = "https://steamcommunity.com/id/{}/gcpd/730?ajax=1&tab=matchhistorycompetitive".format(steamcustomid)
else:  
    CompetitionStatsLink = False

def LangString(langkey):
    try:
        return LangDict[langkey]
    except Exception as e:
        return e

def progressbar(url,path):
    start = time.time() 
    if(proxies['http']=='' and proxies['https']==''):
        response = r.get(url, stream=True) 
    else:
        response = r.get(url, stream=True, proxies=proxies) 
    size = 0    
    chunk_size = 1024  
    content_size = int(response.headers['content-length'])  
    try:
        if response.status_code == 200:   
            print(LangString('info.download.start').format(size = content_size / chunk_size /1024))   
            filepath = path  
            with open(filepath,'wb') as file:   
                for data in response.iter_content(chunk_size = chunk_size):
                    file.write(data)
                    size +=len(data)
                    print('\r'+ LangString('info.download.downloading') +'%s%.2f%%' % ('>'*int(size*50/ content_size), float(size / content_size * 100)) ,end=' ')
        end = time.time()
        print('\n' + LangString('info.download.complete') % (end - start))
    except Exception as e:
        print( LangString('warn.download.failed').format(e))

if steamcustomid == '' and steamid64 != 0:
    CompetitionStatsLink = "https://steamcommunity.com/profile/{}/gcpd/730?ajax=1&tab=matchhistorycompetitive".format(steamid64)
elif steamcustomid != '':
    CompetitionStatsLink = "https://steamcommunity.com/id/{}/gcpd/730?ajax=1&tab=matchhistorycompetitive".format(steamcustomid)
else:  
    CompetitionStatsLink = False

def Download():
    global CompetitionStatsLink
    if not CompetitionStatsLink:
        print(LangString('error.idnotset'))
        sys.exit()
    if(proxies['http']=='' and proxies['https']==''):
        print(LangString('warn.proxies.disabled'))
        CompetitionList = r.get(CompetitionStatsLink, headers=headers).text
    else:
        print(LangString('info.proxies.enabled'))
        proxyenabled=True
        CompetitionList = r.get(CompetitionStatsLink, proxies=proxies, headers=headers).text
    while True:
        LinkList=[]
        LinkList = re.findall(r'"http:\\\/\\\/replay141\.valve\.net\\\/730\\\/................................\.dem\.bz2', CompetitionList)
        if LinkList == []:
            print(LangString('info.download.nodemo').format(delay))
            if steamcustomid == '' and steamid64 != 0:
                CompetitionStatsLink = "https://steamcommunity.com/profile/{}/gcpd/730?ajax=1&tab=matchhistorycompetitive".format(steamid64)
            elif steamcustomid != '':
                CompetitionStatsLink = "https://steamcommunity.com/id/{}/gcpd/730?ajax=1&tab=matchhistorycompetitive".format(steamcustomid)
            else:  
                CompetitionStatsLink = False
            time.sleep(delay)
        try:
            continuetoken = str(re.findall(r'\"continue_token\"\:\"[0-9]+\"', CompetitionList)[0]).replace('"','').replace('continue_token:','')
            print(LangString('info.continuetoken.set'))
        except:
            print(LangString('warn.continuetoken.notfound'))
        for link in LinkList:
            filelink=link
            filename=link[40:]
            if os.path.exists('./Demo/'+filename):
                print(LangString('info.file.exists').format(filename))
            else:
                print(LangString('info.file.downloading').format(filename,filelink.replace('\\','').replace('"','')))
                progressbar(filelink.replace('\\','').replace('"',''),'./Demo/'+filename)
                # with open('./Demo/'+filename,'wb+') as f:
                #     f.write(r.get(filelink.replace('\\','').replace('"','')).content)
                #     f.close
        if previousdownload:
            print(LangString('info.previousdl.enabled'))
            if proxyenabled:
                CompetitionList = r.get(CompetitionStatsLink+'&continue_token={}&sessionid={}'.format(continuetoken,sessionid),proxies=proxies,headers=headers).text
            else:
                CompetitionList = r.get(CompetitionStatsLink+'&continue_token={}&sessionid={}'.format(continuetoken,sessionid),headers=headers).text
        else:
            print(LangString('info.previousdl.disabled'))
            print(LangString('info.download.nodemo').format(delay))
            time.sleep(delay)
            

if __name__ == '__main__':
    WelcomeMsg=LangString('info.welcomemsg')
    print(WelcomeMsg)
    Download()
    input("\n" + LangString('tips.continue'))