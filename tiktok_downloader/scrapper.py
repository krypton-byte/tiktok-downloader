from __future__ import annotations
from typing import Any, Callable, Dict, List, Tuple
import requests
from re import Pattern
import json
from datetime import datetime
from .Except import InvalidUrl
import re


def pattern1(js: dict) -> dict[str, Any]:
    return js


def pattern2(js: dict) -> dict[str, Any]:
    true = js.get('props', {}).get('pageProps', {}).get('itemInfo')
    if true:
        return js
    h = {
        "props": {
            "pageProps": {
                "itemInfo": {
                    "itemStruct": {
                        "author": list(js['UserModule']['users'].values())[0],
                        **list(js['ItemModule'].values())[0]
                    },
                }
            }
        },
        "query": {
            "$initialProps": js['AppContext']['appContext']
        }
    }
    return h


pattern = [
    (re.compile(i), f) for i, f in [
        (r'\>(\{\"props\":.*?)\<\/script>', pattern1),
        (r'window\[\'SIGI_STATE\'\]\=(.*?\});', pattern2)
    ]
]


def regex(inspect: str) -> Dict[Pattern, Dict]:
    def loop(rg: List[Tuple[Pattern, Callable]]):
        for pattern, func in rg:
            try:
                y = func(json.loads(pattern.search(inspect).group(1)))
                return {pattern: y}
            except Exception:
                continue
        else:
            raise InvalidUrl()
    return loop(pattern)


def RequestTikTok(
    f: Callable[[
            info_post,
            Dict[str, Any], Dict[str, Any]
        ],
        None
    ]
):
    def req(object: info_post, url: str) -> None:
        headers: dict = {
            "sec-ch-ua": '"Google Chrome";v="89", '
            '"Chromium";v="89", '
            '";Not A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "origin": "https://tiktok.com",
            "referer": "https://tiktok.com",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/89.0.4389.90 Safari/537.36"
        }
        html = requests.get(url, headers=headers)
        for pattern, rregex in regex(html.text).items():
            y = pattern.search(html.text)
            if y:
                return f(object, rregex, y[0])
        raise InvalidUrl()
    return req


class info_post:
    '''
    :param url: video url(tiktok)
    '''
    BASE_URL = 'https://www.tiktok.com'

    @RequestTikTok
    def __init__(self, js: dict, full: dict) -> None:
        self.full = full
        self.js = js
        if not self.js['props']['pageProps'].get('itemInfo'):
            status_code = self.js['props']['pageProps'].get("statusCode", 0)
            raise InvalidUrl("error_" + str(status_code))
        if not (
            self.js['props']['pageProps']
            ['itemInfo']['itemStruct'].get('challenges')
        ):
            print(self.js)
            self.account = (self.js['props']
                    ['pageProps']['itemInfo']
                    ['itemStruct']['author']
                ) if isinstance(self.js['props']
                    ['pageProps']['itemInfo']
                    ['itemStruct']['author'], str
                ) else Account(
                (
                    self.js['props']
                    ['pageProps']['itemInfo']
                    ['itemStruct']
                )
            )
        self.video = self.js['props']['pageProps']['itemInfo']['itemStruct']
        self.cover = self.video['video']['cover']
        self.music = self.video['music']['title']
        self.nickname = self.video.get(
            'nickname',
            list(set(re.findall(
                r'"nickname"\:".*?"',
                full.__str__())))[0])
        self.caption = self.video['desc']
        self.create = datetime.fromtimestamp(int(self.video['createTime']))
        (
            self.id,
            self.height,
            self.width,
            self.duration,
            self.ratio,
            self.bitrate
        ) = (
            self.video['video']['id'],
            self.video['video']['height'],
            self.video['video']['width'],
            self.video['video']['duration'],
            self.video['video']['ratio'],
            self.video['video']['bitrate']
        )
        self.url = f"{self.BASE_URL}/{self.nickname}/video/{self.id}"
        self.tt_csrf_token = self.js['query']['$initialProps']['$csrfToken']
        self.aftercsrf = self.js['query']['$initialProps']['$encryptedWebid']
        self.tt_webid_v2 = self.js['query']['$initialProps'].get('$logId')
        # self.headers.update(
        #     {
        #         'Cookie': f'tt_webid_v2={self.tt_webid_v2}; \
        #             tt_csrf_token={self.tt_csrf_token}; \
        #             {self.aftercsrf}'
        #     }
        # )

    def __str__(self) -> str:
        return f"<(ID:{self.id})>"

    def __repr__(self) -> str:
        return self.__str__()


class Account:

    def __init__(self, js: dict) -> None:
        self.avatar = js.get('avatarThumb')
        self.username = js.get('uniqueId')
        self.nickname = js.get('nickname')
        self.signature = js.get('signature')
        self.create = datetime.fromtimestamp(int(js.get('createTime', 0)))
        self.verified = js.get('verified')
        self.private = js.get("privateAccount")

    def __repr__(self) -> str:
        return f"<(OWNER:{self.username} VERIFIED:{self.verified})>"

    def __str__(self) -> str:
        return self.__repr__()
