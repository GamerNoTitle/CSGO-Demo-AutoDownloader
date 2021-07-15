from csgo.sharecode import decode 
from pprint import pprint
from steam.client import SteamClient
from csgo.client import CSGOClient as cs

# client = SteamClient()
# csgo = cs(client)

# @client.on('logged_on')
# def start_csgo():
#     csgo.launch()

# @csgo.on('ready')
# def gc_ready():
#     # send messages to gc
#     pass

# client.anonymous_login()
# client.run_forever()

def decoder(link):
    code = link.replace('steam://rungame/730/76561202255233023/+csgo_download_match%20','')
    result = decode(code)
    return result

if __name__ == '__main__':
    while True:
        link = input('Please input your link: ')
        result = decoder(link)
        pprint(result)
        matchid,outcomeid,token = result['matchid'],result['outcomeid'],result['token']
        cs.__init__()
        info = cs.request_full_match_info(self=cs,matchid=matchid,outcomeid=outcomeid,token=token)
        pprint(info)
