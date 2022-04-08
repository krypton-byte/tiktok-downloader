<p align="center">
<img src="tiktok_downloader/static/tiktok.svg"><br>
<img src="https://img.shields.io/badge/AUTHOR-KRYPTON--BYTE-brightgreen">
</p>
<center>
    
[![Unittest](https://github.com/krypton-byte/tiktok-downloader/actions/workflows/unittest.yml/badge.svg)](https://github.com/krypton-byte/tiktok-downloader/actions/workflows/unittest.yml)
[![Upload to PyPi](https://github.com/krypton-byte/tiktok-downloader/actions/workflows/python-publish.yml/badge.svg?branch=0.1.7&event=release)](https://github.com/krypton-byte/tiktok-downloader/actions/workflows/python-publish.yml)
[![Downloads](https://static.pepy.tech/personalized-badge/tiktok-downloader?period=total&units=none&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/tiktok-downloader)
[![viitor](https://visitor-badge.glitch.me/badge?page_id=krypton-byte.tiktok-downloader)]()

</center>

# install

```bash
> python3 -m pip install tiktok_downloader
> python3 -m pip install git+https://github.com/krypton-byte/tiktok-downloader
```

# Library
<details>
<summary>Tikmate</summary>

```python
>>> from tiktok_downloader import Tikmate
>>> d=Tikmate("url")
[<[type: "video" watermark: False]>, <[type: "video" watermark: False]>]
>>> d[0].download('video.mp4')
```

</details>

<details>
<summary>Snaptik</summary>

```python
>>> from tiktok_downloader import Snaptik
>>> d=Snaptik('https://vt.tiktok.com/xxxxxx/')
>>> d
[<[type: "video" watermark: False]>]
>>> d[0].download('video.mp4')
```
</details>

<details>
<summary>Musically Down</summary>

```python
>>> from tiktok_downloader import Mdown
>>> d=Mdown('https://vt.tiktok.com/xxxxxx/')
>>> d
[<[type: "video" watermark: False]>]
>>> d[0].download('video.mp4')
```
</details>

<details>
<summary>Tikdown</summary>

```python
>>> from tiktok_downloader import TikDown
>>> d=TikDown('https://vt.tiktok.com/xxxxxx/')
>>> d
[<[type: "video" watermark: False]>]
>>> d[0].download('video.mp4')
```
</details>

<details>
<summary>TTDownloader</summary>

```python
>>> from tiktok_downloader import ttdownloader
>>> d=ttdownloader'https://vt.tiktok.com/xxxxxx/')
>>> d
[<[type: "video" watermark: False]>]
>>> d[0].download('video.mp4')
```
</details>

<details>
<summary>Tiktok</summary>

```python
>>> from tiktok_downloader import info_post
>>> d=info_post.service('https://vt.tiktok.com/xxxxxx/')
>>> d
[<[type: "video" watermark: False]>]
>>> d[0].download('video.mp4')
```
</details>

<details>
<summary>Get Info</summary>

```python
>>> from tiktok_downloader import info_post
>>> info_post('https://vt.tiktok.com/xxxxxx/')
```
</details>

# Command line

```
usage: python3 -m tiktok_downloader [-h] [--snaptik | --ssstik | --tikmate | --mdown | --ttdownloader | --tikdown | --tiktok] [--host HOST] [--debug] [--port PORT] (--server | --url URL) [--info] [--json | --save SAVE]

Tiktok Downloader [CLI]

options:
  -h, --help      show this help message and exit

List Of Services:
  --snaptik
  --ssstik
  --tikmate
  --mdown
  --ttdownloader
  --tikdown
  --tiktok

Web Configuration:
  --host HOST     Set host to run this web
  --debug         Set flask mode to debug
  --port PORT     Set port

Mode:
  --server        Run as web application
  --url URL       Video URL

Optional:
  --info          Print info video like author, id & etc

Output Type:
  --json          Print result to json format
  --save SAVE     Write the result to file
```
## Example CLI

<details>
<summary>Download</summary>

```bash
$ python3 -m tiktok_downloader --url https://vt.tiktok.com/lorem --snaptik --save tiktok.mp4
```

</details>

<details>
<summary>Json</summary>

```bash
$ python3 -m tiktok_downloader --url https://vt.tiktok.com/lorem --snaptik --json
```

</details>

<details><summary>Run as web</summary>

```bash
$ python3 -m tiktok_downloader --host=0.0.0.0 --port=8000 --server
 * Serving Flask app 'tiktok_downloader.server' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```
</details>

## Deploy Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/krypton-byte/tiktok-downloader/tree/master)
## Preview
<img src="image/web.png">

## Request API using curl & wget

```bash
$ wget -O result.mp4 $(curl -sG http://127.0.0.1:8000/snaptik -d url=https://vm.tiktok.com/xxxxxxxx/|jq .[0].url -r)
```
## you can direct Download using browser or curl
```
http://127.0.0.1:8000/snaptik?url=https://vm.tiktok.com/xxxxxxxx/&type=embed
```
### Endpoint 
| Name | Endpoint | Status|
|----|---------|--------|
| <a href="https://snaptik.app">Snaptik</a> | /snaptik | ✓
| <a href="https://tikmate.online">Tikmate</a> | /tikmate |✓
| <a href="https://musicaldown.com/">MusicalDown | /mdown|✓
| <a href="https://ssstik.io">ssstik</a> | /ssstik | x
| <a href="https://ttdownloader.com/">ttdownloader</a> | /ttdownloader | ✓
| <a href="https://tikdown.org/">tikdown</a> | /tikdown | ✓
| <a href="https://tiktok.com/">tiktok</a> | /tiktok | ✓
# Donasi
<p align="center"><img src="https://svgur.com/i/Vtt.svg">

</p>
<ul><li><a href="https://saweria.co/kryptonbyte">Saweria</a><li><a href="https://wa.me/6283172366463">Whatsapp</a></li><li><a href="https://trakteer.id/krypton-byte-z8vbo">Trakteer</a></li></ul>
