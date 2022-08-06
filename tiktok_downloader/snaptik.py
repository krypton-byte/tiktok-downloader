from sys import stderr
from ast import literal_eval
from .utils import info_videotiktok
from .Except import InvalidUrl
from requests import Session
from re import findall
from .decoder import decoder


class snaptik(Session):
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
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/86.0.4240.111 Safari/537.36'
            }
        self.resp = self.get(
            'https://snaptik.app/abc.php',
            params={
                'url': tiktok_url,
                'lang': 'en',
                **dict(
                    findall(
                        'name="(token)" value="(.*?)"',
                        self.get('https://snaptik.app/en').text))},
        )
        if 'error_api_web;' in self.resp.text or 'Error:' in self.resp.text:
            raise InvalidUrl()

    def get_media(self) -> list[info_videotiktok]:
        '''
        ```python
        >>> <snaptik object>.get_media()
        [<[type:video]>, <[type:video]>]
        ```
        '''
        stderr.flush()
        dec = decoder(*literal_eval(
            findall(
                r'\(\".*?,.*?,.*?,.*?,.*?.*?\)',
                self.resp.text
            )[0]
        ))

        stderr.flush()
        return [
            info_videotiktok(
                i,
                self
            )
            for i in set(['https://snaptik.app'+x.strip('\\') for x in findall(
                r'(/file.php?.*?)\"',
                dec
            )] + [i.strip('\\') for i in findall(
                r'\"(https?://snapxcdn.*?)\"',
                dec
            )])
        ]

    def __iter__(self):
        yield from self.get_media()


def Snaptik(url: str):
    return snaptik(url).get_media()
