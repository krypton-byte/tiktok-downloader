import requests, json
from datetime import datetime
import re
from tiktok_downloader.Except import InvalidUrl
class info_post(requests.Session):
    '''
    :param url: video url(tiktok)
    '''
    def __init__(self, url: str) -> None:
        super().__init__()
        self.headers={"sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',"sec-ch-ua-mobile": "?0","sec-ch-ua-platform": "Linux","sec-fetch-dest": "document","sec-fetch-mode": "navigate","sec-fetch-site": "none","sec-fetch-user": "?1","upgrade-insecure-requests": "1","user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
        self.html = self.get(url)
        self.js = json.loads(re.search(r'\>(\{\"props\":.*?)\<\/script>',self.html.text).group(1))
        self.account = Account(self.js['props']['pageProps']['itemInfo']['itemStruct']['author'])
        self.video = self.js['props']['pageProps']['itemInfo']['itemStruct']
        self.cover = self.video['video']['cover']
        self.music = self.video['music']['title']
        self.caption = self.video['desc']
        self.create = datetime.fromtimestamp(self.video['createTime'])
        self.url = url
        self.id, self.height, self.width, self.duration, self.ratio,self.bitrate = self.video['video']['id'], self.video['video']['height'],self.video['video']['width'],self.video['video']['duration'],self.video['video']['ratio'],self.video['video']['bitrate']
        self.tt_csrf_token=self.js['query']['$initialProps']['$csrfToken']
        self.aftercsrf=self.js['query']['$initialProps']['$encryptedWebid']
        self.tt_webid_v2=self.js['query']['$initialProps']['$logId']
        self.headers.update({'Cookie':f'tt_webid_v2={self.tt_webid_v2}; tt_csrf_token={self.tt_csrf_token}; {self.aftercsrf}'})
    def __str__(self) -> str:
        return f"<(ID:{self.id})>"
    def __repr__(self) -> str:
        return self.__str__()

class Account:
    def __init__(self, js:dict) -> None:
        self.avatar = js['avatarThumb']
        self.username = js['uniqueId']
        self.nickname = js['nickname']
        self.signature = js['signature']
        self.create = datetime.fromtimestamp(js['createTime'])
        self.verified = js['verified']
        self.private = js["privateAccount"]
    def __repr__(self) -> str:
        return f"<(OWNER:{self.username} VERIFIED:{self.verified})>"
    def __str__(self) -> str:
        return self.__repr__()
