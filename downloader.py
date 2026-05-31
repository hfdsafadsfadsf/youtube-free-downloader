import sys
from pathlib import Path
from yt_dlp import YoutubeDL

PROJECT_DIR = Path(__file__).parent
URLS_FILE = PROJECT_DIR / "urls.txt"
CHANNELS_FILE = PROJECT_DIR / "channels.txt"
DOWNLOAD_DIR = PROJECT_DIR / "downloads"
FAILED_FILE = PROJECT_DIR / "failed.txt"
ARCHIVE_FILE = PROJECT_DIR / "archive.txt"

DOWNLOAD_DIR.mkdir(exist_ok=True)


def read_lines(path):
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]


def write_lines(path, lines):
    with open(path, "w", encoding="utf-8") as f:
        for u in lines:
            f.write(u + "\n")


def append_failed(url, reason):
    with open(FAILED_FILE, "a", encoding="utf-8") as f:
        f.write(f"{url}  # {reason}\n")


def base_opts():
    return {
        "format": "bestvideo[height<=2160]+bestaudio/best[height<=2160]/best",
        "merge_output_format": "mp4",
        "retries": 5,
        "fragment_retries": 5,
        "concurrent_fragment_downloads": 4,
        "ignoreerrors": False,
        "download_archive": str(ARCHIVE_FILE),  # не качать то, что уже есть
    }


def download_single(url):
    opts = base_opts()
    opts["outtmpl"] = str(DOWNLOAD_DIR / "%(title).200B [%(id)s].%(ext)s")
    opts["noplaylist"] = True  # для одиночных ссылок не разворачивать в плейлист
    with YoutubeDL(opts) as ydl:
        ydl.download([url])


def download_channel(url):
    opts = base_opts()
    # для каналов кладём в подпапку с именем канала / плейлиста
    opts["outtmpl"] = str(
        DOWNLOAD_DIR / "%(uploader,playlist_title|канал)s" / "%(title).200B [%(id)s].%(ext)s"
    )
    opts["ignoreerrors"] = True  # если одно видео в канале сдохло — продолжаем дальше
    with YoutubeDL(opts) as ydl:
        ydl.download([url])


def process_singles():
    urls = read_lines(URLS_FILE)
    if not urls:
        print("urls.txt пустой или нет — пропускаю одиночные видео\n")
        return

    print(f"=== одиночные видео: {len(urls)} ===")
    remaining = urls.copy()

    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] качаю: {url}")
        try:
            download_single(url)
            remaining.remove(url)
            write_lines(URLS_FILE, remaining)
            print(f"✓ готово, осталось одиночных: {len(remaining)}")
        except KeyboardInterrupt:
            print("\nостановлено пользователем. прогресс сохранён.")
            sys.exit(0)
        except Exception as e:
            print(f"✗ ошибка: {e}")
            append_failed(url, str(e)[:200])


def process_channels():
    channels = read_lines(CHANNELS_FILE)
    if not channels:
        print("channels.txt пустой или нет — пропускаю каналы\n")
        return

    print(f"\n=== каналы / плейлисты: {len(channels)} ===")

    for i, url in enumerate(channels, 1):
        print(f"\n[канал {i}/{len(channels)}] обрабатываю: {url}")
        try:
            download_channel(url)
            print(f"✓ канал готов: {url}")
        except KeyboardInterrupt:
            print("\nостановлено пользователем.")
            sys.exit(0)
        except Exception as e:
            print(f"✗ ошибка на канале: {e}")
            append_failed(url, f"CHANNEL: {str(e)[:200]}")


def main():
    process_singles()
    process_channels()
    print("\nвсё обработано 🚀")


if __name__ == "__main__":
    main()