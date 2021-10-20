from bs4 import BeautifulSoup
from requests.sessions import Session
from tiktok_downloader.Except import InvalidUrl
from tiktok_downloader.utils import info_videotiktok
class keeptiktok:
    def __init__(self, url) -> None:
        self.request = Session()
        self.base_url = "https://keeptiktok.com/"
        self.headers = {"sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',"sec-ch-ua-mobile": "?0","sec-fetch-dest": "document","sec-fetch-mode": "navigate","sec-fetch-site": "none","sec-fetch-user": "?1","upgrade-insecure-requests": "1","user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
        self.url = url
        self.token = BeautifulSoup(self.request.get(self.base_url, headers=self.headers).text, "html.parser").find_all("input", attrs={"id":"token"})[0]["value"]
    def get_info(self):
        try:
            headers = {"origin": "https://keeptiktok.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "referer": "https://keeptiktok.com/",
            "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "content-type": "application/x-www-form-urlencoded",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
            return [info_videotiktok(BeautifulSoup(self.request.post("https://keeptiktok.com/index.php",headers=headers,  allow_redirects=True,data={"url":self.url, "token":self.token}).text, "html.parser").find_all("source")[0]["src"], self.headers, self.request)]
        except IndexError:
            raise InvalidUrl("URL ERROR")
    def __str__(self) -> str:
        return "<[ METHOD: KEEPTIKTOK] >"
    def __repr__(self) -> str:
        return self.__str__()