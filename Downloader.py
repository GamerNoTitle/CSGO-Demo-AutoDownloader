import json as js
import time
import re
import requests as r
from http.cookies import SimpleCookie
import os
import sys

# import sentry_sdk
# sentry_sdk.init(
#     "https://3a21870186ec4fd5902051bb922a0458@o361988.ingest.sentry.io/5850334",

#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     # We recommend adjusting this value in production.
#     traces_sample_rate=1.0
# )

with open('./config.json', 'r') as f:
    config = js.load(f)
    f.close()

ProgramVersion = '1.0.8'
lang = config['lang']
steamcustomid = config['steam']['steamcustomid']
steamid64 = config['steam']['steamid64']
proxies = config['proxies']
cookie = config['steam']['steamcookie']
encoding = config['encoding']
cookieSimple = SimpleCookie(cookie)
cookieDecoded = {i.key: i.value for i in cookieSimple.values()}
previousdownload = config['previousdownload']
continuetoken = 0
delay = config['delay']
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

try:
    with open('./i18n/{}.json'.format(lang), 'r', encoding=encoding) as langfile:
        LangDict = js.load(langfile)
        langfile.close()
except FileNotFoundError as e:
    print('[ERROR]Language file {}.json not found! The program will run in English.'.format(lang))
    with open('./i18n/en.json'.format(lang), 'r', encoding=encoding) as langfile:
        LangDict = js.load(langfile)
        langfile.close()

if steamcustomid == '' and steamid64 != 0:
    CompetitionStatsLink = "https://steamcommunity.com/profile/{}/gcpd/730?tab=matchhistorycompetitive".format(
        steamid64)
elif steamcustomid != '':
    CompetitionStatsLink = "https://steamcommunity.com/id/{}/gcpd/730?tab=matchhistorycompetitive".format(
        steamcustomid)
else:
    CompetitionStatsLink = False


def LangString(langkey):
    try:
        return LangDict[langkey]
    except Exception as e:
        return e


def progressbar(url, path, proxy):
    start = time.time()
    while True:
        try:
            if(not proxy):
                response = r.get(url, stream=True)
            else:
                response = r.get(url, stream=True, proxies=proxies)
            break
        except Exception as e:
            print(LangString('error.connect.failed.prev')+str(e) +
                  ', '+LangString('error.connect.failed.next'))
            time.sleep(3)
    size = 0
    chunk_size = 1024
    content_size = int(response.headers['content-length'])
    try:
        if response.status_code == 200:
            print(LangString('info.download.start').format(
                size=content_size / chunk_size / 1024))
            filepath = path
            with open(filepath, 'wb') as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)
                    print('\r' + LangString('info.download.downloading') + '%s%.2f%%' %
                          ('>'*int(size*50 / content_size), float(size / content_size * 100)), end=' ')
        end = time.time()
        print('\n' + LangString('info.download.complete') % (end - start))
    except Exception as e:
        print(LangString('warn.download.failed').format(e))

class FiveEPlay():
    def Match(playerID):
        PlayerLink = 'https://arena.5eplay.com/data/player/{}'.format(playerID)
        while True:
            if config['proxies']['enable'] and (config['proxies']['global'] or config['proxies']['site']['5eplay.com']):
                PlayerInfo = r.get(PlayerLink, proxies=proxies)
            else:
                PlayerInfo = r.get(PlayerLink)
            break
        MatchResult = re.findall(re.findall(
            r'https\:\/\/cd\-demo\.5eplaycdn\.com\/pug\/[0-9]+\/g151-n-[0-9]+_.+?\.zip', str(PlayerInfo.content)))
        return MatchResult

    def Download(playerID):
        None


class Steam():
    def Download():
        global CompetitionStatsLink
        if not CompetitionStatsLink:
            # Neither steamid64 nor steamcustomid is not set and this will display
            print(LangString('error.idnotset'))
            input("\n" + LangString('tips.continue'))
            sys.exit()
        if(proxies['enable'] and (proxies['global'] or proxies['site']['steamcommunity.com'])):
            print(LangString('info.proxies.enabled'))
            while True:
                try:
                    CompetitionList = r.get(CompetitionStatsLink,
                                            proxies=proxies, headers=headers).text
                    break
                except Exception as e:
                    print(LangString('error.connect.failed.prev')+str(e) +
                          ', '+LangString('error.connect.failed.next'))
                    time.sleep(3)
        else:
            # When the proxy is disabled, this message will tell the users.
            print(LangString('warn.proxies.disabled'))
            while True:
                try:
                    CompetitionList = r.get(
                        CompetitionStatsLink, headers=headers).text
                    break
                except Exception as e:
                    print(LangString('error.connect.failed.prev')+str(e) +
                          ', '+LangString('error.connect.failed.next'))
                    time.sleep(3)

        while True:
            LinkList = []
            OfficialLinkList = re.findall(
                r'"http:\/\/replay1[0-9][0-9]\.valve\.net\/730\/[0-9]+_[0-9]+\.dem\.bz2', CompetitionList)
            PerfectWorldLinkList = re.findall(
                r'"http:\/\/replay[0-9][0-9][0-9]\.wmsj\.cn\/730\/[0-9]+_[0-9]+\.dem\.bz2', CompetitionList)
            LinkList = OfficialLinkList + PerfectWorldLinkList
            print(OfficialLinkList,PerfectWorldLinkList,LinkList)
            # with open('./SteamCommuntiy.html', 'wt', encoding='utf8') as f:   # Debug
            #     f.write(CompetitionList)
            if LinkList == []:
                # No Demo Message
                print(LangString('info.download.nodemo').format(delay))
                if steamcustomid == '' and steamid64 != 0:
                    CompetitionStatsLink = "https://steamcommunity.com/profile/{}/gcpd/730?&tab=matchhistorycompetitive".format(
                        steamid64)
                elif steamcustomid != '':
                    CompetitionStatsLink = "https://steamcommunity.com/id/{}/gcpd/730?&tab=matchhistorycompetitive".format(
                        steamcustomid)
                else:
                    CompetitionStatsLink = False
                while True:
                    try:
                        if(proxies['enable'] and (proxies['global'] or proxies['site']['steamcommunity.com'])):
                            CompetitionList = r.get(CompetitionStatsLink,
                                                    proxies=proxies, headers=headers).text
                        else:
                            CompetitionList = r.get(
                                CompetitionStatsLink, headers=headers).text
                        break
                    except Exception as e:
                        print(LangString('error.connect.failed.prev')+str(e) +
                              ', '+LangString('error.connect.failed.next'))
                        time.sleep(3)
                break
            else:
                try:
                    continuetoken = str(re.findall(r"var g_sGcContinueToken = \'[0-9]+\';", CompetitionList)[
                                        0]).replace('var g_sGcContinueToken = \'', '').replace('\';', '')
                    print(LangString('info.continuetoken.set'))
                except:
                    print(LangString('warn.continuetoken.notfound'))
            for link in LinkList:
                filelink = link
                filename = link[40:]
                if os.path.exists('./Demo/'+filename):
                    print(LangString('info.file.exists').format(filename))
                else:
                    print(LangString('info.file.downloading').format(
                        filename, filelink.replace('\\', '').replace('"', '')))
                    progressbar(filelink.replace('\\', '').replace(
                        '"', ''), './Demo/'+filename, (proxies['enable'] and (proxies['global'] or proxies['site']['steamcommunity.com'])))
                    # the third one will tell the function whether the proxy mode is enabled.
            if previousdownload:
                print(LangString('info.previousdl.enabled'))
                while True:
                    try:
                        if(proxies['enable'] and (proxies['global'] or proxies['site']['steamcommunity.com'])):
                            CompetitionList = r.get(CompetitionStatsLink+'&continue_token={}&sessionid={}'.format(
                                continuetoken, sessionid), proxies=proxies, headers=headers).text
                        else:
                            CompetitionList = r.get(CompetitionStatsLink+'&continue_token={}&sessionid={}'.format(
                                continuetoken, sessionid), headers=headers).text
                        break
                    except Exception as e:
                        print(LangString('error.connect.failed.prev')+str(e) +
                              ', '+LangString('error.connect.failed.next'))
                        time.sleep(3)
            else:
                print(LangString('info.previousdl.disabled'))
                print(LangString('info.download.nodemo').format(delay))


if __name__ == '__main__':
    WelcomeMsg = LangString('info.welcomemsg')
    print(WelcomeMsg)
    print("Version: " + ProgramVersion, end='\n')
    try:
        sessionid = cookieDecoded['sessionid']
    except KeyError:
        print(LangString('error.sessionid.notfound'))
        input("\n" + LangString('tips.continue'))
        sys.exit()
    while True:
        Steam.Download()
        time.sleep(delay)
        print('\n'+LangString('info.loop.start'))
    input("\n" + LangString('tips.continue'))
