import re
from bs4 import BeautifulSoup
from httpx import AsyncClient
from sys import stderr
from ast import literal_eval
import pyjsparser
from .utils import Download, DownloadAsync, Type, extension_to_type
from .Except import InvalidUrl
from requests import Session
from re import findall
from .decoder import decoder
import cloudscraper
from urllib.parse import urlparse


class Snaptik(Session):
    """
    :param tiktok_url:
    ```python
    >>> tik=snaptik('url')
    >>> tik.get_media()
    [<[type:video]>, <[type:video]>]
    ```
    """

    def __init__(self, tiktok_url: str) -> None:
        super().__init__()
        self.headers: dict[str, str] = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/86.0.4240.111 Safari/537.36"
        }
        self.tiktok_url = tiktok_url

    def render(self, token, interval: int = 1):
        result = self.get('https://snaptik.app/render.php', params={'token': token}).json()
        while True:
            resp = self.get("https://snaptik.app/task.php", params={'token': result['task_id']}).json()
            if resp['progress'] == 100:
                return Download(resp['download_url'], self, Type.VIDEO) 
            
    def get_media(self) -> list[Download]:
        """
        ```python
        >>> <snaptik object>.get_media()
        [<[type:video]>, <[type:video]>]
        ```
        """
        result = []
        resp = cloudscraper.create_scraper().get(
            "https://snaptik.app/abc2.php",
            params={
                "url": self.tiktok_url,
                "lang": "en",
                **dict(
                    findall(
                        'name="(token)" value="(.*?)"',
                        self.get("https://snaptik.app/en").text,
                    )
                ),
            },
        )
        if "error_api_web;" in resp.text or "Error:" in resp.text:
            raise InvalidUrl()
        stderr.flush()
        dec = decoder(
            *literal_eval(findall(r"\(\".*?,.*?,.*?,.*?,.*?.*?\)", resp.text)[0])
        )
        dec = pyjsparser.parse(re.sub(r"(async|await)", "", dec))["body"][0][
            "consequent"
        ]["body"][0]["consequent"]["body"][1]["expression"]["right"]["value"]
        bs = BeautifulSoup(dec)
        for vl in  bs.find_all("div", attrs={"class","video-links"}):
            for a in vl.find_all("a"):
                result.append(Download(a["href"] if a['href'].startswith('http') else 'https://snaptik.app' + a['href'], self, Type.VIDEO))
            for button in vl.find_all("button"):
                try:
                    result.append(Download(button['data-backup'], self, Type.VIDEO))
                except KeyError:
                    result.append(Download('', self, Type.VIDEO, render=lambda invertal: self.render(button['data-token'])))
        result.extend(
            [
                Download(obj["href"], self, Type.IMAGE)
                for obj in bs.find_all(
                    "a", attrs={"data-event": "download_albumPhoto_photo"}
                )
            ]
        )
        return result

    def __iter__(self):
        yield from self.get_media()


class SnaptikAsync(AsyncClient):
    """
    :param tiktok_url:
    ```python
    >>> tik=snaptik('url')
    >>> tik.get_media()
    [<[type:video]>, <[type:video]>]
    ```
    """

    def __init__(self, tiktok_url: str) -> None:
        super().__init__()
        self.headers: dict[str, str] = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/86.0.4240.111 Safari/537.36"
        }
        self.tiktok_url = tiktok_url

    async def get_media(self) -> list[DownloadAsync]:
        """
        ```python
        >>> <snaptik object>.get_media()
        [<[type:video]>, <[type:video]>]
        ```
        """
        resp = await self.get(
            "https://snaptik.app/abc2.php",
            params={
                "url": self.tiktok_url,
                "lang": "en",
                **dict(
                    findall(
                        'name="(token)" value="(.*?)"',
                        (await self.get("https://snaptik.app/en")).text,
                    )
                ),
            },
        )
        if "error_api_web;" in resp.text or "Error:" in resp.text:
            raise InvalidUrl()
        stderr.flush()
        dec = decoder(
            *literal_eval(findall(r"\(\".*?,.*?,.*?,.*?,.*?.*?\)", resp.text)[0])
        )

        stderr.flush()
        return [
            DownloadAsync(i, self)
            for i in set(
                [
                    "https://snaptik.app" + x.strip("\\")
                    for x in findall(r"(/file.php?.*?)\"", dec)
                ]
                + [i.strip("\\") for i in findall(r"\"(https?://snapxcdn.*?)\"", dec)]
            )
        ]

    async def __aiter__(self):
        return await self.get_media()


def snaptik(url: str):
    return Snaptik(url).get_media()


async def snaptik_async(url: str):
    return await SnaptikAsync(url).get_media()
