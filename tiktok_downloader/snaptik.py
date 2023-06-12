from httpx import AsyncClient
from sys import stderr
from ast import literal_eval
from .utils import Download, DownloadAsync
from .Except import InvalidUrl
from requests import Session
from re import findall
from .decoder import decoder
import cloudscraper
from urllib.parse import urlparse


class Snaptik(Session):
    '''
    :param tiktok_url:
    ```python
    >>> tik=snaptik('url')
    >>> tik.get_media()
    [<[type:video]>, <[type:video]>]
    ```
    '''

    def __init__(self, tiktok_url: str) -> None:
        super().__init__()
        self.headers: dict[str, str] = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.111 Safari/537.36'
        }
        self.tiktok_url = tiktok_url

    def get_media(self) -> list[Download]:
        '''
        ```python
        >>> <snaptik object>.get_media()
        [<[type:video]>, <[type:video]>]
        ```
        '''
        resp = cloudscraper.create_scraper().get(
            'https://snaptik.app/abc2.php',
            params={
                'url': self.tiktok_url,
                'lang': 'en',
                **dict(
                    findall(
                        'name="(token)" value="(.*?)"',
                        self.get('https://snaptik.app/en').text))}
        )
        if 'error_api_web;' in resp.text or 'Error:' in resp.text:
            raise InvalidUrl()
        stderr.flush()
        dec = decoder(*literal_eval(
            findall(
                r'\(\".*?,.*?,.*?,.*?,.*?.*?\)',
                resp.text
            )[0]
        ))

        stderr.flush()

        current_url = urlparse(resp.url).scheme + "://" + urlparse(resp.url).netloc
        links_list = [
                i for i in findall(r'<a href=\\"(https?://[\w\./\-&?=]+)', dec)
            ] + [
                current_url + i.strip('\\') for i in findall(r'(/file.php?.*?)\"', dec)
            ]

        # If our video is slideshow - download link will have "?type=dl", so let's move it to the 1 place
        index_to_move = None
        for index, link in enumerate(links_list):
            if "?type=dl" in link:
                index_to_move = index
                break

        # Move the link to the first position (0 index) if found
        if index_to_move is not None:
            links_list.insert(0, links_list.pop(index_to_move))

        return [
            Download(
                i,
                self
            ) for i in links_list
        ]

    def __iter__(self):
        yield from self.get_media()


class SnaptikAsync(AsyncClient):
    '''
    :param tiktok_url:
    ```python
    >>> tik=snaptik('url')
    >>> tik.get_media()
    [<[type:video]>, <[type:video]>]
    ```
    '''

    def __init__(self, tiktok_url: str) -> None:
        super().__init__()
        self.headers: dict[str, str] = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.111 Safari/537.36'
        }
        self.tiktok_url = tiktok_url

    async def get_media(self) -> list[DownloadAsync]:
        '''
        ```python
        >>> <snaptik object>.get_media()
        [<[type:video]>, <[type:video]>]
        ```
        '''
        resp = await self.get(
            'https://snaptik.app/abc2.php',
            params={
                'url': self.tiktok_url,
                'lang': 'en',
                **dict(
                    findall(
                        'name="(token)" value="(.*?)"',
                        (await self.get('https://snaptik.app/en')).text))},
        )
        if 'error_api_web;' in resp.text or 'Error:' in resp.text:
            raise InvalidUrl()
        stderr.flush()
        dec = decoder(*literal_eval(
            findall(
                r'\(\".*?,.*?,.*?,.*?,.*?.*?\)',
                resp.text
            )[0]
        ))

        stderr.flush()
        return [
            DownloadAsync(
                i,
                self
            )
            for i in set(['https://snaptik.app' + x.strip('\\') for x in findall(
                r'(/file.php?.*?)\"',
                dec
            )] + [i.strip('\\') for i in findall(
                r'\"(https?://snapxcdn.*?)\"',
                dec
            )])
        ]

    async def __aiter__(self):
        return await self.get_media()


def snaptik(url: str):
    return Snaptik(url).get_media()


async def snaptik_async(url: str):
    return await SnaptikAsync(url).get_media()
