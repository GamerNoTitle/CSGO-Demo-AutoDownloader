<div align='center'>
    <h1>CSGO-Demo-AutoDownloader</h1>
    <h2>Language</h2>
    English | <a href=''>简体中文</a>
</div>

## What's this

This tool can help you download your CSGO demo after you play the game, and save it in `Demo` folder.

You can download it from [RELEASE](https://github.com/GamerNoTitle/CSGO-Demo-AutoDownloader/releases) page.

## Getting Started

### Get your variables

#### steamid64

You can find it in the address bar of your Steam profile. The following number is the `steamid64`.

For example, my Steam profile link is [https://steamcommunity.com/profiles/76561198309889674/](https://steamcommunity.com/profiles/76561198309889674/). Then the `steamid64` should be 76561198309889674

#### steamcustomid

You can find it in the address bar of you Steam profile (If you set it in your profile). You can also find it when you are trying to edit your profile.

![](https://user-images.githubusercontent.com/28426291/124484129-ab840900-dddd-11eb-83dc-523c59492448.png)

For example, my profile link is [https://steamcommunity.com/id/bili33](https://steamcommunity.com/id/bili33), and the `steamcustomid` should be `bili33`.

#### steamcookie

Open up your browser and visit https://store.steampowered.com, press <kbd>F12</kbd> to start up a developer tool, click on `Network`, and refresh the Steam website, you will find a `store.steampowered.com` on the top of the list.

![](https://user-images.githubusercontent.com/28426291/124483233-ae322e80-dddc-11eb-82a3-09e3e479073e.png)

Click on it, scroll down and you will find a cookie key. And open `Cookie-Coverter.exe` and paste it into it to get the cookie that the config needs. Copy the result that the coverter shows and paste it into your config

#### proxies

If you cannot connect to the steamcommunity.com directly, you can use proxy. You can also use V2ray, Clash or something else.

For example, when I'm using v2rayN, the http proxy of this software is `http://127.0.0.1:10809`, and I should fill the `proxy.http` and `proxy.https` as `http://127.0.0.1:10809`

### Fill the config

When you download the pack from RELEASE page (or clone the source code), you got a `config.json`. Now I am going to tell you the detailed information of the variables

```json
{
    "lang": "en",
    "encoding": "utf8",
    "delay": 3600,
    "steamid64": 0,
    "steamcustomid": "",
    "steamcookie": "",
    "previousdownload": false,
    "proxies": {
        "http": "",
        "https": ""
    }
}

```

| Variable         | Detail                                                       | Required                                               | Variable Type                                                |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------------ |
| lang             | The language you use in this program.                        | √                                                      | String, should be the same as the language file in `i18n` folder |
| encoding         | The encoding method of reading the language file             | √                                                      | Normally leave it as `utf8` will work, or some other encoding methods. |
| delay            | The frequency of the program to check your competition history for one time (Count in SECOND) | √                                                      | Integer greater than 0                                       |
| steamid64        | The 64 bits id of your Steam account, you can check it on [steamid.io](https://steamid.io/) or from your profile page link (e.g. In the link [http://steamcommunity.com/profiles/76561198309889674](http://steamcommunity.com/profiles/76561198309889674), the steamid64 should be 76561198309889674) | × (If `steamcustomid` is filled, this can leave blank) | Integer                                                      |
| steamcustomid    | The custom url you set in your profile editing page (e.g. In the link [https://steamcommunity.com/id/bili33](https://steamcommunity.com/id/bili33), the steamcustomid should be bili33) | × (If you leave it blank, you should fill `steamid64`) | String                                                       |
| steamcookie      | The cookie you use in your browser when you are visiting Steam (Before you fill it, you should convert it by using [my convert tool](https://github.com/GamerNoTitle/CSGO-Demo-AutoDownloader/releases/tag/CookieCoverter)) | √                                                      | String                                                       |
| previousdownload | Whether the program should download your previous competition demo (Since the page can only contain the latest 4 competitions at once, you should tell the program should it download the previous competition except for the latest 4 competitions) | ×                                                      | bool (true/false)                                            |
| proxies          | Whether the program should use proxy to connect to the Steam server and download the demo from valve's server | ×                                                      | String                                                       |

### Run the program

After you fill the config well, you can start the program. The program will search the demo that not outdated and download it in `Demo` folder. You should keep a Demo folder in the path that the program run, or that may cause some errors.

If you get the program from the release page, make sure the `config.json` is at the same place of `CSGO-Demo-AutoDownloader.exe`, or the program cannot read the config.

If you clone the source code, you should install the environment first (`pip install -r requirements.txt` for Windows or `pip3 install -r requirements.txt` for Linux), and you can run it by using `python3 Downloader.py`.

## Bugs found

If you found any bugs, please tell me with an issue to make me know. Thanks♪(･ω･)ﾉ

## Donate

Paypal: https://paypal.me/GamerNoTitle

afdian: https://afdian.net/@GamerNoTitle

Alipay (QR Code): https://cdn.jsdelivr.net/gh/GamerNoTitle/Picture-repo-v1@master/img/Payments/AliPay.jpg

WechatPay (QR Code): https://cdn.jsdelivr.net/gh/GamerNoTitle/Picture-repo-v1@master/img/Payments/WeChat.png

## Reference

Progress Bar: https://blog.csdn.net/weixin_43347550/article/details/105248223

