from sys import stderr
from .utils import info_videotiktok
from py_mini_racer import MiniRacer
from .Except import InvalidUrl
from requests import Session
from re import findall
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
    decoder.eval('var _0xc38e = [\n    "",\n    "split",\n    "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/",\n    "slice",\n    "indexOf",\n    "",\n    "",\n    ".",\n    "pow",\n    "reduce",\n    "reverse",\n    "0",\n  ];\n  function _0xe48c(d, e, f) {\n    var g = _0xc38e[2][_0xc38e[1]](_0xc38e[0]);\n    var h = g[_0xc38e[3]](0, e);\n    var i = g[_0xc38e[3]](0, f);\n    var j = d[_0xc38e[1]](_0xc38e[0])\n      [_0xc38e[10]]()\n      [_0xc38e[9]](function (a, b, c) {\n        if (h[_0xc38e[4]](b) !== -1)\n          return (a += h[_0xc38e[4]](b) * Math[_0xc38e[8]](e, c));\n      }, 0);\n    var k = _0xc38e[0];\n    while (j > 0) {\n      k = i[j % f] + k;\n      j = (j - (j % f)) / f;\n    }\n    return k || _0xc38e[11];\n  }\n  \n  function decoder(h, u, n, t, e, r) {\n    r = "";\n    for (var i = 0, len = h.length; i < len; i++) {\n      var s = "";\n      while (h[i] !== n[e]) {\n        s += h[i];\n        i++;\n      }\n      for (var j = 0; j < n.length; j++) s = s.replace(new RegExp(n[j], "g"), j);\n      r += String.fromCharCode(_0xe48c(s, e, 10) - t);\n    }\n    return decodeURIComponent(escape(r));\n  }')
    def __init__(self, tiktok_url:str) -> None:
        super().__init__()
        self.resp = self.get('https://snaptik.app/abc.php', params={'url':tiktok_url,'lang':'en'}, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'})
        if 'error_api_web;' in self.resp.text or 'Error:' in self.resp.text:
            raise InvalidUrl()
    def get_media(self)->list[info_videotiktok]:
        '''
        ```python
        >>> <snaptik object>.get_media()
        [<[type:video]>, <[type:video]>]
        ```
        '''
        stderr.flush()
        d=eval(findall('\(\".*?,.*?,.*?,.*?,.*?.*?\)',self.resp.text)[0]).__str__()
        dec = self.decoder.eval(f"decoder{d}")
        stderr.flush()
        return [info_videotiktok(i, self) for i in set(map(lambda x:x[0].strip('\\'),findall('\"(https?://(tikcdn\.net|snapsave\.info).*?)\"',dec)))]