import requests
from pathlib import Path


DATA_URL = "https://data.gov.ua/dataset/8733e5b6-a46b-4c1d-bc94-bae88e83c859/resource/cd3d62d6-23c5-49ed-9224-9f4baebb37c8/download/drrro.csv"


BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)

FILE_PATH = DATA_DIR / "drrro.csv"


def download_dataset(url: str, path: Path):
    try:
        print(f"Downloading dataset from {url} ...")

        headers = {"User-Agent": "Mozilla/5.0"}
        with requests.get(url, stream=True, timeout=60, headers=headers) as response:
            response.raise_for_status()

            with open(path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

        print(f"Файл успішно збережено як: {path}")

    except Exception as e:
        print(f"Помилка завантаження: {e}")


if __name__ == "__main__":
    download_dataset(DATA_URL, FILE_PATH)