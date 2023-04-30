from httpx import AsyncClient
from bs4 import BeautifulSoup
import requests
from requests.models import InvalidURL
from .utils import Download, DownloadAsync


class Mdown(requests.Session):
    BASE_URL = 'https://musicaldown.com/'

    def __init__(self) -> None:
        super().__init__()
        self.headers: dict[str, str] = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
        }

    def get_media(self, url: str):
        bs = BeautifulSoup(self.get(self.BASE_URL).text, 'html.parser')
        form = {
            i['name']: i['value'] for i in bs.find_all(
                'input',
                attrs={'type': 'hidden'}
            )
        }
        form.update({bs.find('input', attrs={'type': 'text'})['name']: url})
        res = self.post(
            f'{self.BASE_URL}download',
            data=form,
            headers={
                "origin": "https://musicaldown.com",
                "referer": "https://musicaldown.com/en",
                "sec-ch-ua": '"Chromium";v="94", "Google Chrome";v="94", '
                '";Not A Brand";v="99"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "Linux",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
            }
        )
        if 'err' in res.url:
            raise InvalidURL()
        return [
            Download(
                i['href'],
                self
            ) for i in BeautifulSoup(
                res.text,
                'html.parser'
            ).find_all('a', attrs={'target': '_blank'})
            if i['href'].strip('/').count('/') > 2
        ]


class MdownAsync(AsyncClient):
    BASE_URL = 'https://musicaldown.com/'

    def __init__(self) -> None:
        super().__init__()
        self.headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
        }

    async def get_media(self, url: str):
        html = (await self.get(self.BASE_URL, follow_redirects=True))
        bs = BeautifulSoup(
            html.text, 'html.parser')
        form = {
            i['name']: i['value'] for i in bs.find_all(
                'input',
                attrs={'type': 'hidden'}
            )
        }
        form.update({bs.find('input', attrs={'type': 'text'})['name']: url})
        res = await self.post(
            f'{self.BASE_URL}download',
            data=form,
            headers={
                "origin": "https://musicaldown.com",
                "referer": "https://musicaldown.com/en/",
                "sec-ch-ua": '"Chromium";v="94", "Google Chrome";v="94", '
                '";Not A Brand";v="99"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "Linux",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
            }
        )
        if 'err' in res.url.path:
            raise InvalidURL()
        return [
            DownloadAsync(
                i['href'],
                self
            ) for i in BeautifulSoup(
                res.text,
                'html.parser'
            ).find_all('a', attrs={'target': '_blank'})
        ]


def mdown(url: str):
    return Mdown().get_media(url)


async def mdown_async(url: str):
    return await MdownAsync().get_media(url)
