from io import BytesIO
from typing import Optional, Union
from requests import Session
from tqdm.rich import tqdm
from warnings import simplefilter
from time import sleep
from io import BufferedWriter
simplefilter('ignore')


class Odummy:
    def __init__(self):
        pass

    def f(self, *arg, **kwarg):
        return None

    def __enter__(self):
        return self

    def __exit__(self, type, val, trace):
        return False

    def __getattr__(self, name):
        return self.f


class info_videotiktok:

    def __init__(
        self,
        url: str,
        Session: Session,
        type='video',
        watermark: bool = False
    ) -> None:
        self.json = url
        self.type = type
        self.Session = Session
        self.watermark = watermark

    def get_size(self) -> int:
        return int(
            self.Session.get(
                self.json,
                stream=True
            ).headers["Content-Length"]
        )

    def download(
        self,
        out: Optional[Union[str, BufferedWriter]] = None,
        chunk_size=1024,
        bar=False
    ) -> Union[None, BytesIO, BufferedWriter]:
        request = self.Session.get(self.json, stream=True)
        stream = out if isinstance(
            out,
            BufferedWriter) else (
                open(out, 'wb') if isinstance(
                    out,
                    str) else BytesIO())
        if request.headers.get('content-length'):
            with tqdm(
                total=int(request.headers['Content-Length']),
                unit='iB',
                    unit_scale=True) if bar else Odummy() as pbar:
                for i in request.iter_content(chunk_size):
                    stream.write(i)
                    pbar.update(i.__len__())
                pbar.update(int(request.headers['Content-Length']))
                if not isinstance(pbar, Odummy):
                    sleep(1)
        else:
            stream.write(request.content)
        return None if isinstance(out, (str, BufferedWriter)) else stream

    def __str__(self) -> str:
        f = (
            self.type == 'video' and f' \
watermark: {self.watermark}]>') or ']>'
        return f"<[type: \"{self.type}\""+f

    def __repr__(self) -> str:
        return self.__str__()
