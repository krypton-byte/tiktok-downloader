from requests import Session
import re
from .utils import info_videotiktok


class TKDown(Session):
    BASE_URL = 'https://tikdown.org/'
    headers = {
        "origin": 'https://tikdown.org',
        "referer": 'https://tikdown.org/',
        "sec-ch-ua": '"Chromium";v="94", '
        '"Google Chrome";v="94", ";Not A Brand";v="99"',
        "sec-ch-ua-mobile": '?0',
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": 'empty',
        "sec-fetch-mode": 'cors',
        "sec-fetch-site": 'same-origin',
        "user-agent": 'Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/94.0.4606.81 Safari/537.36',
        "x-requested-with": 'XMLHttpRequest'
    }

    def __init__(self, url: str) -> None:
        super().__init__()
        self.url = url

    def get_media(self) -> list[info_videotiktok]:
        res = self.get(self.BASE_URL)
        _token = re.findall(
            r'type\="hidden".*?value\="([0-9a-zA-Z]+)"',
            res.text
        )[0]
        self.headers.update({'x-csrf-token': _token})
        js = self.post(self.BASE_URL+'getAjax', data={
            'url': self.url,
            '_token': _token
        }).json()
        if js.get('status'):
            video = re.findall(
                r'\"(https?://.*?\.mp4)\"',
                js['html']
            )[0]
            return [info_videotiktok(video, self)]
        return []


def TikDown(url: str):
    return TKDown(url).get_media()
