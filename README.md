# youtube-free-downloader

Скачивает видео с YouTube (и других сайтов) в максимальном качестве до 4K. Поддерживает одиночные видео, плейлисты и целые каналы. Не скачивает одно и то же дважды.

## Установка

1. Установи Python 3.8+
2. Установи зависимости:

pip install yt-dlp


## Использование

### Одиночные видео
Добавь ссылки в `urls.txt` (по одной на строку):

https://youtube.com/watch?v=...
https://youtube.com/watch?v=...


### Каналы и плейлисты
Добавь ссылки в `channels.txt` (по одной на строку):

https://youtube.com/@channelname
https://youtube.com/playlist?list=...


### Запуск

python downloader.py


Видео сохраняются в папку `downloads/`.
Одиночные — прямо в папку, каналы — в подпапку с именем канала.

## Особенности

- Качество до 4K (2160p), формат MP4
- Архив уже скачанного — повторно не качает (`archive.txt`)
- Если видео не скачалось — записывается в `failed.txt`
- При ошибке на одном видео канала — продолжает дальше
- Можно остановить в любой момент (Ctrl+C) — прогресс сохранится

---

# youtube-free-downloader

Downloads videos from YouTube (and other sites) in the best quality up to 4K. Supports single videos, playlists, and entire channels. Never downloads the same video twice.

## Installation

1. Install Python 3.8+
2. Install dependencies:

pip install yt-dlp


## Usage

### Single videos
Add links to `urls.txt` (one per line):

https://youtube.com/watch?v=...
https://youtube.com/watch?v=...


### Channels and playlists
Add links to `channels.txt` (one per line):

https://youtube.com/@channelname
https://youtube.com/playlist?list=...


### Run

python downloader.py


Videos are saved to the `downloads/` folder.
Single videos go directly into the folder, channels get their own subfolder.

## Features

- Up to 4K quality (2160p), MP4 format
- Download archive — never re-downloads the same video (`archive.txt`)
- Failed downloads are logged to `failed.txt`
- If one video in a channel fails — continues with the rest
- Stop anytime with Ctrl+C — progress is saved
