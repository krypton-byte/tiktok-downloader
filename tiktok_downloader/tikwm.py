from httpx import AsyncClient
from requests import Session
from requests.models import InvalidURL
from .utils import Download, DownloadAsync, Type


class TikWM(Session):
    BASE_URL = 'https://www.tikwm.com'

    def __init__(self, url: str) -> None:
        super().__init__()
        self.url = url

    def get_media(self) -> list[Download]:
        req = self.post(self.BASE_URL + '/api/', data=dict(url=self.url, count=12, cursor=0, web=1, hd=1))
        res = req.json()
        if res['code'] == 0:
            return [
                Download(
                    self.BASE_URL + res['data'].get('hdplay', res['data']['play']),
                    self,
                    Type.VIDEO
                ),
                Download(
                    self.BASE_URL + res['data']['wmplay'],
                    self,
                    'video',
                    Type.VIDEO
                ),
                Download(
                    self.BASE_URL + res['data']['music'],
                    self,
                    Type.AUDIO
                )
            ]
        else:
            raise InvalidURL(res['msg'])


class TikWMAsync(AsyncClient):
    BASE_URL = 'https://www.tikwm.com'

    def __init__(self, url: str) -> None:
        super().__init__(follow_redirects=True)
        self.url = url

    async def get_media(self) -> list[DownloadAsync]:
        req = await self.post(self.BASE_URL + '/api/', data=dict(url=self.url, count=12, cursor=0, web=1, hd=1))
        res = req.json()
        if res['code'] == 0:
            return [
                DownloadAsync(
                    self.BASE_URL + res['data'].get('hdplay', res['data']['play']),
                    self,
                    Type.VIDEO
                ),
                DownloadAsync(
                    self.BASE_URL + res['data']['wmplay'],
                    self,
                    Type.VIDEO,
                    True
                ),
                DownloadAsync(
                    self.BASE_URL + res['data']['music'],
                    self,
                    Type.AUDIO
                )
            ]
        else:
            raise InvalidURL(res['msg'])


def tikwm(url: str) -> list[Download]:
    return TikWM(url).get_media()


async def tikwm_async(url: str) -> list[DownloadAsync]:
    return await TikWMAsync(url).get_media()