import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from pathlib import Path


def run_visualization():

    DB_PATH = Path("/app/data/database.sqlite")

    OUTPUT_PATH = Path("/app/reports/figures")
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    if not DB_PATH.exists():
        print(f"Базу даних не знайдено: {DB_PATH}")
        return

    print(f"Завантаження даних з БД для візуалізації...")
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM rro_data", conn)
    conn.close()


    df['updates_count'] = df['dateAndNumberTheInclusionDecision'].str.count('від').fillna(0)


    plt.figure(figsize=(10, 6))
    top_applicants = df['applicant'].value_counts().head(5).index
    data_h2 = df[df['applicant'].isin(top_applicants)].groupby('applicant')['updates_count'].mean().sort_values()

    names = [str(n).replace('\n', ' ').strip()[:30] + '...' for n in data_h2.index]

    plt.barh(names, data_h2.values, color='skyblue')
    plt.title('Середня кількість оновлень ПЗ (ТОП-5 заявників)')
    plt.xlabel('Кількість рішень ДПС')
    plt.tight_layout()

    file1 = OUTPUT_PATH / "top_applicants_activity.png"
    plt.savefig(file1)
    plt.close()
    print(f"Збережено: {file1}")


    plt.figure(figsize=(8, 8))
    mfr_counts = df['manufacturer'].value_counts()
    top_3 = mfr_counts.head(3)
    others = pd.Series({'Інші виробники': mfr_counts.iloc[3:].sum()})
    pie_data = pd.concat([top_3, others])

    plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    plt.title('Розподіл ринку між виробниками РРО')
    plt.tight_layout()

    file2 = OUTPUT_PATH / "market_share.png"
    plt.savefig(file2)
    plt.close()
    print(f"Збережено: {file2}")

    print(f"Візуалізацію успішно завершено.")


if __name__ == "__main__":
    run_visualization()