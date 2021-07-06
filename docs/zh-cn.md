<div align='center'>
    <h1>CSGO-Demo-AutoDownloader</h1>
</div>

这是一个能够帮助你自动下载CSGO官匹Demo并保存在`Demo`文件夹内的开箱即用的小工具。

你可以从 [RELEASE](https://github.com/GamerNoTitle/CSGO-Demo-AutoDownloader/releases) 页面获取这个工具。

## 开始使用

### 获取配置

#### steamid64

你可以在你的Steam个人资料页面的地址栏找到`steamid64`这个变量（其实就是Steam的64位个人ID）

例如，我的Steam个人资料链接是[https://steamcommunity.com/profiles/76561198309889674/](https://steamcommunity.com/profiles/76561198309889674/) 那么`steamid64`的值就应该是`76561198309889674`

#### steamcustomid

你可以在Steam个人资料页面的地址栏找到`steamcustomid`这个变量（前提是你设置了，就是自定义URL）。

![](https://user-images.githubusercontent.com/28426291/124484129-ab840900-dddd-11eb-83dc-523c59492448.png)

例如，我的Steam个人资料链接是[https://steamcommunity.com/id/bili33](https://steamcommunity.com/id/bili33) ，那么`steamcustomid`的值就应该为`bili33`.

#### steamcookie

打开你的浏览器并访问~~https://store.steampowered.com~~ https://steamcommunity.com ，按下 <kbd>F12</kbd> 来打开开发者工具，点击`Network`（网络），然后刷新网页, 你会在顶部找到一条 ~~`store.steampowered.com`~~ `steamcommunity.com`的记录（**一定要是社区的Cookie**）

![](https://user-images.githubusercontent.com/28426291/124483233-ae322e80-dddc-11eb-82a3-09e3e479073e.png)

点击它，向下拉会看到Cookie的值，复制它，然后打开附带的`Cookie-Coverter.exe`并将复制的cookie贴进去来转换成配置中需要的cookie，复制转换的结果填入`steamcookie`的值里面。 

#### proxies

身为天朝用户，我们不能够直接连接`steamcommunity.com`，有的人可能会使用[SteamCommunity302](https://www.dogfight360.com/blog/686/)或者是[Steam++](https://steampp.net/)一类的辅助工具，这种就不要设置代理，但是要把社区加速打开

但是，例如我，不习惯用这些，反而习惯用V2rayN、Clash这一类的代理工具，那就需要设置Proxies这个值。举个栗子，V2rayN的默认配置的代理是`http://127.0.0.1:10809`（Socks5是10808但是我们用不到Socks5，不要填错了），就把`http://127.0.0.1:10809`填入`http`和`https`的后面就行了

### 填写配置

当你从RELEASE页面下载软件（或者直接Clone源代码），会附带一个`config.json`。接下来我将告诉你具体的变量及其作用。

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

| 变量名称         | 具体信息                                                     | 必需                                                 | 变量类型                                                     |
| ---------------- | ------------------------------------------------------------ | ---------------------------------------------------- | ------------------------------------------------------------ |
| lang             | 使用程序过程中所展示的语言                                   | √                                                    | 字符串，但是填写的内容应该能够在`i18n`文件夹找到对应的文件，中文用户请填写`zh-cn` |
| encoding         | 程序读取语言文件时所采用的编码方式                           | √                                                    | 一般来说直接填`utf8`就可以了，也可以填其他的编码方式（但是可能会造成无法读取的问题） |
| delay            | 程序读取竞技比赛记录的频率（单位：秒/次）                    | √                                                    | 大于0的整数                                                  |
| steamid64        | Steam的64位用户ID，你可以在[steamid.io](https://steamid.io/) 查询，也可以在自己的个人资料页找到(例如：我的个人资料页的链接是[http://steamcommunity.com/profiles/76561198309889674](http://steamcommunity.com/profiles/76561198309889674)，那么steamid64的值就是`76561198309889674`) | × (如果填写了`steamcustomid`，可以不填，保留默认值0) | 整数                                                         |
| steamcustomid    | Steam自定义URL的值 (例如：我的个人资料页的链接是[https://steamcommunity.com/id/bili33](https://steamcommunity.com/id/bili33)，那么steamcustomid的值就是`bili33`) | × (如果此处不填，那么`steamid64`必填)                | 字符串                                                       |
| steamcookie      | 你在访问Steam页面时所使用的的Cookie (填写之前一定要用 [转换工具](https://github.com/GamerNoTitle/CSGO-Demo-AutoDownloader/releases/tag/CookieCoverter) 进行转换，否则无法使用) | √                                                    | 字符串                                                       |
| previousdownload | 程序是否应该下载除了第一页所展示的四场比赛以外的比赛（因为V社在个人比赛记录里面一页只显示4场，故有此配置项） | ×                                                    | 布尔型（true/false）                                         |
| proxies          | 程序在连接`steamcommunity.com`和V社Demo服务器时使用的代理    | ×                                                    | 字符串                                                       |

### 使用程序

当你填写完了配置，你就可以打开本程序了。程序将会搜索V社服务器上未过期的Demo并自动下载到`Demo`文件夹。你需要保证程序运行目录中有`Demo`文件夹，否则会造成不必要的麻烦。

如果你是从RELEASE页面下载的程序，请注意将所有的压缩包中的内容放在同一文件夹下，否则程序可能无法运行。

如果你是使用的源码，你需要先安装python环境和必要的轮子(Windows：`pip install -r requirements.txt` | Linux：`pip3 install -r requirements.txt`)然后再使用`python Downloader.py`或者`python3 Downloader.py`来运行程序。

## BUG反馈

如果你发现了BUG，请提交issue来告诉我，Thanks♪(･ω･)ﾉ

## 捐赠（要恰饭的嘛）

Paypal: https://paypal.me/GamerNoTitle

爱发电: https://afdian.net/@GamerNoTitle

支付宝（二维码）: https://cdn.jsdelivr.net/gh/GamerNoTitle/Picture-repo-v1@master/img/Payments/AliPay.jpg

微信（二维码）: https://cdn.jsdelivr.net/gh/GamerNoTitle/Picture-repo-v1@master/img/Payments/WeChat.png

## 参考

下载进度条: https://blog.csdn.net/weixin_43347550/article/details/105248223
