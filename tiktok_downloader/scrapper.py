from requests import Session
import requests, json
from datetime import datetime
from bs4 import BeautifulSoup
import re
from tiktok_downloader.Except import InvalidUrl
from tiktok_downloader.keeptiktok import keeptiktok
from tiktok_downloader.utils import info_videotiktok
class info_post(requests.Session):
    def __init__(self, url: str) -> None:
        super().__init__()
        '''
        :param url: video url(tiktok)
        '''
        self.headers={"sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',"sec-ch-ua-mobile": "?0","sec-ch-ua-platform": "Linux","sec-fetch-dest": "document","sec-fetch-mode": "navigate","sec-fetch-site": "none","sec-fetch-user": "?1","upgrade-insecure-requests": "1","user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
        self.html = self.get(url)
        self.js = json.loads(re.search('\>(\{\"props\":.*?)\<\/script>',self.html.text).group(1))
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
class tiktok:
    def __init__(self, url) -> None:
        self.request = Session()
        self.header  = {"content-type": "application/x-www-form-urlencoded; charset=UTF-8","hx-active-element": "submit","hx-current-url": "https://ssstik.io/","hx-request": "true","hx-target": "target","origin": "https://ssstik.io","sec-fetch-dest": "","sec-fetch-mode": "cors","sec-fetch-site": "same-origin","user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"}
        self.url     = "https://ssstik.io"
        self.html    = self.request.get(self.url, headers=self.header).text
        #self.key     = BeautifulSoup(self.html, "html.parser").find_all("form",attrs={"data-hx-target":"#target"})[0].get("include-vals")
        #self.post    = BeautifulSoup(self.html, "html.parser").find_all("form",attrs={"data-hx-target":"#target"})[0].get("data-hx-post")
        #self.tt      = re.search("tt\:\'(.*?)\'",self.key)[1]
        #self.ts      = re.search("ts\:([0-9]{5,15})",self.key)[1]
        self.url_vid = url
        
    def get_info(self):
        try:
            data   = {"id": self.url_vid,"locale": "en","tt": 0,"ts": 0}
            post   = self.request.post(self.url+re.findall('data-hx-post=\"(.*?)\"',self.html)[0], headers=self.header, data=data)
            respon = BeautifulSoup(post.text, "html.parser")
            #return post
            self.hasil  = {"video":[f'{self.url}{respon.find_all("a",class_="pure-button pure-button-primary is-center u-bl dl-button download_link without_watermark")[0].get("href")}',f'{self.url}{respon.find_all("a",class_="pure-button pure-button-primary is-center u-bl dl-button download_link without_watermark_direct")[0].get("href")}'],"music":f'{respon.find_all("a",class_="pure-button pure-button-primary is-center u-bl dl-button download_link music")[0].get("href")}'}
            return [info_videotiktok(x, self.header, self.request) for x in self.hasil["video"]]
        except IndexError:
            raise InvalidUrl("URL ERROR")
    def __str__(self) -> str:
        return "<[ Method: ssstik.io ]>"
    def __repr__(self) -> str:
        return self.__str__()
class tiktok2:
    def __init__(self, url) -> None:
        self.request = Session()
        self.url = url
        self.header  = {"accept": "*/*","accept-language": "en-US,en;q=0.9,id;q=0.8","origin": "https://snaptik.app","referer": "https://snaptik.app/ID","sec-fetch-dest": None,"sec-fetch-mode": "cors","sec-fetch-site": "same-origin","user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",}
    def get_info(self):
        try:
            self.request.post("https://snaptik.app/check_token.php", headers=self.header)
            self.php = re.findall(', \"(.*?\.php)',requests.get("https://snaptik.app", headers=self.header).text)[0]
            self.bs = BeautifulSoup(self.request.post(f"https://snaptik.app/{self.php}", headers=self.header, data={"url":self.url}).text, "html.parser")
            self.hasil=[self.request,{"title":self.bs('a', attrs={"title":""})[0].text,"date":self.bs("b", attrs={"class":"blur"})[0].text,"video":list(filter(lambda x:x, map(lambda x:x["href"] if "token" in x["href"] else None, self.bs("a", attrs={"class":"abutton is-success is-fullwidth"}))))}, self.header]
            return [info_videotiktok(x, self.header, self.request) for x in self.hasil[1]["video"]]
        except IndexError:
            raise InvalidUrl("URL ERROR")
    def __str__(self) -> str:
        return "<[ Method: Snaptik.io ]>"
    def __repr__(self) -> str:
        return self.__str__()
class Tiktok:
    info_video = info_post
    ssstik = tiktok
    snaptik = tiktok2
    keeptiktok = keeptiktok
    def __str__(self) -> str:
        return "<[ Tiktok Downloader No Watermark Scraper]>"
    def __repr__(self) -> str:
        return self.__str__()