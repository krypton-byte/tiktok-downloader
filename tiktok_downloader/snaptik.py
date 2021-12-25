from sys import stderr
from ast import literal_eval
from .utils import info_videotiktok
from py_mini_racer import MiniRacer
from .Except import InvalidUrl
from requests import Session
from re import findall
from os.path import dirname


class snaptik(Session):
    '''
    :param tiktok_url:
    ```python
    >>> tik=snaptik('url')
    >>> tik.get_media()
    [<[type:video]>, <[type:video]>]
    ```
    '''
    decoder = MiniRacer()
    decoder.eval(
        open(dirname(__file__)+'/decoder.js', 'r').read()
    )

    def __init__(self, tiktok_url: str) -> None:
        super().__init__()
        self.resp = self.get(
            'https://snaptik.app/abc.php',
            params={'url': tiktok_url, 'lang': 'en'},
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/86.0.4240.111 Safari/537.36'
            }
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
        d = literal_eval(
            findall(
                r'\(\".*?,.*?,.*?,.*?,.*?.*?\)',
                self.resp.text
            )[0]
        ).__str__()
        dec = self.decoder.eval(f"decoder{d}")
        stderr.flush()
        return [
            info_videotiktok(
                i,
                self
            )
            for i in set(
                map(
                    lambda x:x[0].strip('\\'),
                    findall(
                        r'\"(https?://(tikcdn\.net|snapsave\.info).*?)\"',
                        dec
                    )
                )
            )
        ]

    def __iter__(self):
        yield from self.get_media()
