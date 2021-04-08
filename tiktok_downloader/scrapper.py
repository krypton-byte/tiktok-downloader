from io import BytesIO
from requests import Session
from bs4 import BeautifulSoup
import re
from tiktok_scrapper.Except import InvalidUrl
class info_videotiktok:
    def __init__(self,  url, headers,request) -> None:
        self.json = url
        self.request = request
        self.headers = headers
    def get_size(self):
        return int(self.request.get(self.json, headers=self.headers, stream=True).headers["Content-Length"])
    def download(self, out=False):
        if isinstance(out, str):
            open(out, "wb").write(self.request.get(self.json,headers=self.headers).content)
        else:
            return BytesIO(self.request.get(self.json,headers=self.headers).content)
    def __str__(self) -> str:
        return f"<[type:video]>"
    def __repr__(self) -> str:
        return self.__str__()

class Tiktok:
    def __init__(self, url):
        self.none = None
        self.ssstik = tiktok2(url)
        self.snaptik = tiktok2(url)
    def __str__(self) -> str:
        return "<[ Tiktok Downloader No Watermark Scraper]>"
    def __repr__(self) -> str:
        return self.__str__()
class tiktok:
    def __init__(self, url) -> None:
        self.request = Session()
        self.url     = "https://ssstik.io"
        self.html    = self.request.get(self.url).text
        self.key     = BeautifulSoup(self.html, "html.parser").find_all("form",attrs={"data-hx-target":"#target"})[0].get("include-vals")
        self.post    = BeautifulSoup(self.html, "html.parser").find_all("form",attrs={"data-hx-target":"#target"})[0].get("data-hx-post")
        self.tt      = re.search("tt\:\'(.*?)\'",self.key)[1]
        self.ts      = re.search("ts\:([0-9]{5,15})",self.key)[1]
        self.url_vid = url
        self.header  = {"content-type": "application/x-www-form-urlencoded; charset=UTF-8","hx-active-element": "submit","hx-current-url": "https://ssstik.io/","hx-request": "true","hx-target": "target","origin": "https://ssstik.io","sec-fetch-dest": "","sec-fetch-mode": "cors","sec-fetch-site": "same-origin","user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"}
    def get_info(self):
        try:
            data   = {"id": self.url_vid,"locale": "en","tt": self.tt,"ts": int(self.ts)}
            post   = self.request.post(f"{self.url}{self.post}", headers=self.header, data=data)
            respon = BeautifulSoup(post.text, "html.parser")
            self.hasil  = {"video":[f'{self.url}{respon.find_all("a",class_="pure-button pure-button-primary is-center u-bl dl-button download_link without_watermark")[0].get("href")}',f'{self.url}{respon.find_all("a",class_="pure-button pure-button-primary is-center u-bl dl-button download_link without_watermark_direct")[0].get("href")}'],"music":f'{respon.find_all("a",class_="pure-button pure-button-primary is-center u-bl dl-button download_link music")[0].get("href")}'}
            return [info_videotiktok(x, self.header, self.request) for x in self.hasil["video"]]
        except IndexError:
            raise InvalidUrl("URL ERROR")
    def __str__(self) -> str:
        return "<[ Method: sstik.io ]>"
    def __repr__(self) -> str:
        return self.__str__()
class tiktok2:
    def __init__(self, url) -> None:
        self.request = Session()
        self.url =url
        self.header  = {"accept": "*/*","accept-language": "en-US,en;q=0.9,id;q=0.8","origin": "https://snaptik.app","referer": "https://snaptik.app/ID","sec-fetch-dest": None,"sec-fetch-mode": "cors","sec-fetch-site": "same-origin","user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",}
    def get_info(self):
        try:
            self.request.post("https://snaptik.app/check_token.php", headers=self.header)
            self.bs = BeautifulSoup(self.request.post("https://snaptik.app/action-2021.php", headers=self.header, data={"url":self.url}).text, "html.parser")
            self.hasil=[self.request,{"title":self.bs('a', attrs={"title":""})[0].text,"date":self.bs("b", attrs={"class":"blur"})[0].text,"video":list(filter(lambda x:x, map(lambda x:x["href"] if "token" in x["href"] else None, self.bs("a", attrs={"class":"abutton is-success is-fullwidth"}))))}, self.header]
            return [info_videotiktok(x, self.header, self.request) for x in self.hasil[1]["video"]]
        except IndexError:
            raise InvalidUrl("URL ERROR")
    def __str__(self) -> str:
        return "<[ Method: Snaptik.io ]>"
    def __repr__(self) -> str:
        return self.__str__()