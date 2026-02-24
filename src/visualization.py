import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import re


def run_visualization():
    BASE_DIR = Path(__file__).resolve().parents[1]
    raw_path = BASE_DIR / "data" / "raw" / "drrro.csv"
    output_path = BASE_DIR / "reports" / "figures"
    output_path.mkdir(parents=True, exist_ok=True)

    if not raw_path.exists():
        return

    df = pd.read_csv(raw_path, sep=';', encoding='utf-8', quotechar='"', engine='python')

    df['updates_count'] = df['dateAndNumberTheInclusionDecision'].str.count('від').fillna(0)


    plt.figure(figsize=(10, 6))
    top_applicants = df['applicant'].value_counts().head(5).index
    data_h2 = df[df['applicant'].isin(top_applicants)].groupby('applicant')['updates_count'].mean().sort_values()

    names = [n.replace('\n', ' ').strip()[:30] + '...' for n in data_h2.index]

    plt.barh(names, data_h2.values, color='skyblue')
    plt.title('Середня кількість оновлень ПЗ (ТОП-5 заявників)')
    plt.xlabel('Кількість рішень ДПС')
    plt.tight_layout()
    plt.savefig(output_path / "top_applicants_activity.png")
    plt.close()


    plt.figure(figsize=(8, 8))
    mfr_counts = df['manufacturer'].value_counts()
    top_3 = mfr_counts.head(3)
    others = pd.Series({'Інші виробники': mfr_counts.iloc[3:].sum()})
    pie_data = pd.concat([top_3, others])

    plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    plt.title('Розподіл ринку між виробниками РРО')
    plt.tight_layout()
    plt.savefig(output_path / "market_share.png")
    plt.close()

    print(f"Візуалізацію завершено. Графіки збережено в: {output_path}")


if __name__ == "__main__":
    run_visualization()