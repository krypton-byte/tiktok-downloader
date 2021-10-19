from requests import Session
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re
from tiktok_downloader.Except import InvalidUrl
from tiktok_downloader.keeptiktok import keeptiktok
from tiktok_downloader.utils import info_videotiktok
class info_post:
    def __init__(self, url: str) -> None:
        '''
        :param url: video url(tiktok)
        '''
        self.html = requests.get(url,headers={"sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',"sec-ch-ua-mobile": "?0","sec-fetch-dest": "document","sec-fetch-mode": "navigate","sec-fetch-site": "none","sec-fetch-user": "?1","upgrade-insecure-requests": "1","user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"})
        self.account = Account(self.html)
        self.music = re.findall("music\"\:.*?\"title\"\:\"(.*?)\"", self.html.text)[0]
        self.caption = BeautifulSoup(self.html.text, "html.parser").title.text
        self.create = datetime.fromtimestamp(int(re.findall("\"createTime\"\:(.*?),", self.html.text)[0]))
        self.url = re.findall("\"canonicalHref\"\:\"(.*?)\"", self.html.text)[0]
        self.id, self.height, self.width, self.duration, self.ratio = re.findall("\"video\"\:\{\"id\"\:\"(.*?)\",\"height\":(.*?),\"width\"\:(.*?),\"duration\":(.*?),\"ratio\"\:\"(.*?)\",", self.html.text)[0]
    def __str__(self) -> str:
        return ""
        #return f"<(ID:{self.id})>"
    def __repr__(self) -> str:
        return self.__str__()
class Account:
    def __init__(self, html) -> None:
        self.html =html
        self.username = re.findall("\"uniqueId\"\:\"(.*?)\"", self.html.text)[0] if re.findall("\"uniqueId\"\:\"(.*?)\"", self.html.text) else None
        self.nickname = re.findall("\"nickname\"\:\"(.*?)\"", self.html.text)[0] if re.findall("\"nickname\"\:\"(.*?)\"", self.html.text) else None
        self.signature = re.findall("\"signature\"\:\"(.*?)\"", self.html.text)[0] if re.findall("\"signature\"\:\"(.*?)\"", self.html.text) else None
        self.create = datetime.fromtimestamp(int(re.findall("\"createTime\"\:(.*?),", self.html.text)[1])) if len(re.findall("\"createTime\"\:(.*?),", self.html.text))>=2 else None
        self.verified = False if re.findall("\"verified\"\:(.*?),", self.html.text)[0]=="false" else True if re.findall("\"verified\"\:(.*?),", self.html.text) else None
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