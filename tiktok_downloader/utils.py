from __future__ import annotations
import httpx
from io import BytesIO
from typing import Optional, Union
from requests import Session
from warnings import simplefilter
from io import BufferedWriter
simplefilter('ignore')


class DownloadCallback:
    def __init__(self) -> None:
        self.finished = False

    async def on_open(
        self,
        client: httpx.AsyncClient,
        response: httpx.Response,
        info: DownloadAsync
    ):
        raise NotImplementedError()

    async def on_progress(self, binaries: bytes):
        raise NotImplementedError()

    async def on_finish(
        self,
        client: httpx.AsyncClient,
        response: httpx.Response
    ):
        raise NotImplementedError()


class DownloadAsync:

    def __init__(
        self,
        url: str,
        Session: httpx.AsyncClient,
        type='video',
        watermark: bool = False
    ) -> None:
        self.json = url
        self.type = type
        self.Session = Session
        self.watermark = watermark

    async def get_size(self) -> int:
        return int((
            await self.Session.stream(
                'GET',
                self.json
            ).__aenter__()
        ).headers["Content-Length"])

    async def download(
        self,
        out: Optional[Union[str, BufferedWriter, DownloadCallback]] = None,
        chunk_size=1024
    ) -> Union[None, BytesIO, BufferedWriter, DownloadCallback]:
        async with self.Session.stream('GET', self.json) as request:
            if isinstance(out, DownloadCallback):
                await out.on_open(self.Session, request, self)
            stream = out if isinstance(
                out,
                BufferedWriter) else (
                    open(out, 'wb') if isinstance(
                        out,
                        str) else BytesIO())
            if isinstance(out, DownloadCallback):
                async for i in request.aiter_bytes(chunk_size):
                    await out.on_progress(i)
            else:
                async for i in request.aiter_bytes(chunk_size):
                    stream.write(i)
            if isinstance(out, DownloadCallback):
                out.finished = True
            return None if isinstance(
                out, (
                    str,
                    BufferedWriter
                    )) else out if isinstance(
                        out, DownloadCallback) else stream

    def __str__(self) -> str:
        f = (
            self.type == 'video' and f' \
watermark: {self.watermark}]>') or ']>'
        return f"<[type: \"{self.type}\""+f

    def __repr__(self) -> str:
        return self.__str__()


class Download:

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
        for i in request.iter_content(chunk_size):
            stream.write(i)
        return None if isinstance(out, (str, BufferedWriter)) else stream

    def __str__(self) -> str:
        f = (
            self.type == 'video' and f' \
watermark: {self.watermark}]>') or ']>'
        return f"<[type: \"{self.type}\""+f

    def __repr__(self) -> str:
        return self.__str__()
