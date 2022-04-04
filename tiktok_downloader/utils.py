from io import BytesIO
from typing import Optional, Union
from requests import Session


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

    def download(self, out: Optional[str] = None, chunk_size = 1024) -> Union[None, BytesIO]:
        request = self.Session.get(self.json, stream=True)
        with (open(out,'wb') if isinstance(out, str) else BytesIO()) as stream:
            for i in request.iter_content(chunk_size):
                stream.write(i)
            return None if isinstance(out, str) else stream

    def __str__(self) -> str:
        f = (
            self.type == 'video' and f' \
watermark: {self.watermark}]>') or ']>'
        return f"<[type: \"{self.type}\""+f

    def __repr__(self) -> str:
        return self.__str__()
