import requests
from pathlib import Path
import pandas as pd
import sqlite3
import os

DATA_URL = "https://data.gov.ua/dataset/8733e5b6-a46b-4c1d-bc94-bae88e83c859/resource/cd3d62d6-23c5-49ed-9224-9f4baebb37c8/download/drrro.csv"


DATA_DIR = Path("/app/data")
RAW_DIR = DATA_DIR / "raw"
DB_PATH = DATA_DIR / "database.sqlite"
FILE_PATH = RAW_DIR / "drrro.csv"


def download_and_store():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    try:
        print(f"Downloading dataset ...")
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(DATA_URL, timeout=60, headers=headers)
        response.raise_for_status()

        with open(FILE_PATH, "wb") as f:
            f.write(response.content)
        print(f"CSV збережено: {FILE_PATH}")


        print("Імпортуємо дані в SQLite...")

        df = pd.read_csv(FILE_PATH, sep=';', encoding='utf-8', quotechar='"', engine='python')


        conn = sqlite3.connect(DB_PATH)

        df.to_sql('rro_data', conn, if_exists='replace', index=False)
        conn.close()

        print(f"БД успішно створена за шляхом: {DB_PATH}")

    except Exception as e:
        print(f"Помилка завантаження: {e}")


if __name__ == "__main__":
    download_and_store()