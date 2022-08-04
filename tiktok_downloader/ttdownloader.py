from requests import Session
import re
from .utils import info_videotiktok


class TTDownloader(Session):
    BASE_URL = 'https://ttdownloader.com/'

    def __init__(self, url: str) -> None:
        super().__init__()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 '
            'Safari/537.36',
            'origin': 'https://ttdownloader.com',
            'referer': 'https://ttdownloader.com/',
            'sec-ch-ua': '"Chromium";v="94",'
            '"Google Chrome";v="94", ";'
            'Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Linux",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'x-requested-with': 'XMLHttpRequest'
        }
        self.url = url

    def get_media(self) -> list[info_videotiktok]:
        indexsource = self.get(self.BASE_URL)
        token = re.findall(r'value=\"([0-9a-z]+)\"', indexsource.text)
        result = self.post(
            self.BASE_URL+'query/',
            data={'url': self.url, 'format': '', 'token': token[0]}
        )
        nowm, wm, audio = re.findall(
            r'(https?://.*?.php\?v\=.*?)\"', result.text
        )
        return [
            info_videotiktok(nowm, self, 'video'),
            info_videotiktok(wm, self, 'video', True),
            info_videotiktok(audio, self, 'music')
        ]


def ttdownloader(url: str) -> list[info_videotiktok]:
    return TTDownloader(url).get_media()
