import time
from bs4 import BeautifulSoup
from cloudscraper import (
    create_scraper,
    Session
)
import re
from .utils import info_videotiktok
from requests.models import InvalidURL


class ssstik(Session):
    '''
    :param delay:
    ```python
    >>> tik=ssstik()
    >>> tik.get_media('....')
    [<[type:video]>, <[type:video]>, <[type:music]>]
    ```
    '''
    BASE = "https://ssstik.io"
    HEADERS = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "hx-active-element": "submit",
        "hx-current-url": "https://ssstik.io/",
        "hx-request": "true",
        "hx-target": "target",
        "origin": "https://ssstik.io",
        "sec-fetch-dest": "",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"}

    def __init__(self, delay: int = 10, **kwargs) -> None:
        super().__init__(**kwargs)
        self.headers = self.HEADERS
        self.cf = create_scraper(delay=delay)
        self.html = self.cf.get(self.BASE)
        while True:
            if self.html.status_code == 403:
                print('retrying request')
                self.cf = create_scraper(delay=delay)
                self.html = self.cf.get(self.BASE)
                time.sleep(5)
            else:
                break

    def get_media(self, url: str) -> list[info_videotiktok]:
        '''
        :param url:
        ```python
        >>> <ssstik object>.get_media('....')
        [<[type:video]>, <[type:video]>]
        ```
        '''
        try:
            post = self.cf.post(
                self.BASE+re.findall(
                    'hx-post=\"(.*?)\"',
                    self.html.text
                )[0],
                data={
                    "id": url,
                    "locale": "en",
                    "tt": 0,
                    "ts": 0
                }
            )
            respon = BeautifulSoup(post.text, "html.parser")
            hasil = [
                *[
                    info_videotiktok(
                        url=i,
                        Session=self.cf,
                        type='video'
                    )
                    for i in [
                        self.BASE+respon.find_all(
                            "a",
                            class_="pure-button pure-button-primary \
                                is-center u-bl dl-button download_link \
                                without_watermark")[0].get("href"),
                        respon.find_all(
                            "a",
                            class_="pure-button pure-button-primary \
                                is-center u-bl dl-button download_link \
                                without_watermark_direct")[0].get("href")
                        ]
                ],
                info_videotiktok(
                    respon.find_all(
                        "a",
                        class_="pure-button pure-button-primary is-center \
                            u-bl dl-button download_link music"
                    )[0].get("href"),
                    Session=self.cf,
                    type='music'
                )
            ]
            return hasil
        except IndexError:
            raise InvalidURL()


def Ssstik(url: str, delay=10):
    return ssstik(delay).get_media(url)
