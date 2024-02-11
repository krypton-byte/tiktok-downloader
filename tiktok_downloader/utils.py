from __future__ import annotations
import asyncio
import httpx
from PIL import Image
from moviepy.video.VideoClip import tempfile
import numpy as np
from io import BytesIO
from typing import Callable, List, Optional, Union
from moviepy.audio.AudioClip import concatenate_audioclips
from requests import Session
from warnings import simplefilter
from io import BufferedWriter
from enum import Enum
from moviepy.editor import (
    CompositeAudioClip,
    ImageClip,
    AudioFileClip,
    CompositeVideoClip,
    VideoClip,
    concatenate_videoclips,
    transfx,
)
import re
from tiktok_downloader.Except import NoImageToSlideshow
from concurrent.futures import ThreadPoolExecutor

simplefilter("ignore")

def extension_to_type(filename: str):
    if re.search(r'\.mp3$', filename):
        return Type.AUDIO
    elif re.search(r'\.jpg$', filename):
        return Type.IMAGE
    elif re.search(r'\.mp4$', filename):
        return Type.VIDEO
    raise ValueError()

class Type(Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"
    SLIDESHOW = "SLIDESHOW"


class DownloadCallback:
    def __init__(self) -> None:
        self.finished = False

    async def on_open(
        self, client: httpx.AsyncClient, response: httpx.Response, info: DownloadAsync
    ):
        raise NotImplementedError()

    async def on_progress(self, binaries: bytes):
        raise NotImplementedError()

    async def on_finish(self, client: httpx.AsyncClient, response: httpx.Response):
        raise NotImplementedError()


def render_from_images(
    images: List[str | BytesIO], audio_file: str, outfile: str, fps: int = 30, *args, **kwargs
):
    img_pil = []
    max_height = 0
    max_width = 0
    for img in images:
        _img = Image.open(img).convert("RGB")
        if _img.height > max_height:
            max_height = _img.height
        if _img.width > max_width:
            max_width = _img.height
        img_pil.append(_img)
    new_img = Image.new("RGB", (max_width, max_height), (255, 255, 255))
    for idx, img in enumerate(img_pil):
        new_frame = new_img.copy()
        new_frame.paste(
            img, ((max_width - img.width) // 2, (max_height - img.height) // 2)
        )
        img_pil[idx] = new_frame
    audio = AudioFileClip(audio_file)
    duration_clip = audio.duration / images.__len__()
    frames = [ImageClip(np.array(im), duration=duration_clip) for im in img_pil]
    video = concatenate_videoclips(frames)
    video.set_audio(audio)
    video.audio = CompositeAudioClip([audio])
    video.write_videofile(filename=outfile, fps=fps, *args, **kwargs)


class RenderImageToSlidshow:
    def __init__(self, download: List[DownloadAsync] | List[Download]) -> None:
        self.list_image = [i for i in download if i.type == Type.IMAGE]
        self.audio = [i for i in download if i.type == Type.AUDIO][0]
        if not self.list_image:
            raise NoImageToSlideshow()

    def render(self, outfile: str,worker: int = 2):
        with ThreadPoolExecutor(max_workers=worker) as thread:
            result = list(thread.map(lambda x: x.download(BytesIO()), self.list_image))
            with tempfile.TemporaryFile(mode='wb', delete=True) as file:
                self.audio.download(file)
                file.close()
                render_from_images(result, file.name, outfile=outfile)

                
    async def render_async(self, image,executor: Optional[ThreadPoolExecutor] = None):
        new_loop = asyncio.new_event_loop()
        result = []
        futures =[]
        for d in self.list_image:
            result.append(BytesIO())
            futures.append(d.download(result[-1]))
        await asyncio.gather(*futures)
        with tempfile.TemporaryFile(mode="wb", delete=True) as file:
            self.audio.download(file)
            return await new_loop.run_in_executor(executor, render_from_images, (result, file.name))


class DownloadAsync:
    def __init__(
        self,
        url: str,
        Session: httpx.AsyncClient,
        type=Type.VIDEO,
        watermark: bool = False,
    ) -> None:
        self.json = url
        self.type = type
        self.Session = Session
        self.watermark = watermark

    async def get_size(self) -> int:
        return int(
            (await self.Session.stream("GET", self.json).__aenter__()).headers[
                "Content-Length"
            ]
        )

    async def download(
        self,
        out: Optional[Union[str, BufferedWriter, DownloadCallback]] = None,
        chunk_size=1024 * 1024,
    ) -> Union[None, BytesIO, BufferedWriter, DownloadCallback]:
        async with self.Session.stream("GET", self.json) as request:
            if isinstance(out, DownloadCallback):
                await out.on_open(self.Session, request, self)
            stream = (
                out
                if isinstance(out, BufferedWriter)
                else (open(out, "wb") if isinstance(out, str) else BytesIO())
            )
            if isinstance(out, DownloadCallback):
                tasks = []
                async for i in request.aiter_bytes(chunk_size):
                    tasks.append(asyncio.ensure_future(out.on_progress(i)))
                await asyncio.gather(*tasks)
            else:
                async for i in request.aiter_bytes(chunk_size):
                    stream.write(i)
            if isinstance(out, DownloadCallback):
                out.finished = True
                await out.on_finish(self.Session, request)
            return (
                None
                if isinstance(out, (str, BufferedWriter))
                else out
                if isinstance(out, DownloadCallback)
                else stream
            )

    def __str__(self) -> str:
        return f'<type: "{self.type.value}" watermark:"{self.watermark}">'

    def __repr__(self) -> str:
        return self.__str__()


class Download:
    def __init__(
        self, url: str, Session: Session, type=Type.VIDEO, render: Optional[Callable] = None, watermark: bool = False
    ) -> None:
        self.json = url
        self.type = type
        self.render = render
        self.Session = Session
        self.watermark = watermark
    def get_render(self, interval: int = 1) -> Download | None:
        if self.render:
            return self.render(interval)
    def get_size(self) -> int:
        return int(self.Session.get(self.json, stream=True).headers["Content-Length"])

    def download(
        self,
        out: Optional[Union[str, BufferedWriter]] = None,
        chunk_size=1024,
        bar=False,
    ) -> Union[None, BytesIO, BufferedWriter]:
        request = self.Session.get(self.json, stream=True)
        stream = (
            out
            if isinstance(out, BufferedWriter)
            else (open(out, "wb") if isinstance(out, str) else BytesIO())
        )
        for i in request.iter_content(chunk_size):
            stream.write(i)
        return None if isinstance(out, (str, BufferedWriter)) else stream

    def __str__(self) -> str:
        return f'<[type: "{self.type}" watermark: "{self.watermark}" render: "{bool(self.render)}">' 

    def __repr__(self) -> str:
        return self.__str__()
