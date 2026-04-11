import pandas as pd
from pathlib import Path
import re
import warnings

warnings.filterwarnings('ignore')

def run_drrro_research():
    BASE_DIR = Path(__file__).resolve().parents[1]
    raw_path = BASE_DIR / "data" / "raw" / "drrro.csv"

    if not raw_path.exists():
        print(f"Файл не знайдено: {raw_path}")
        return

    df = pd.read_csv(raw_path, sep=';', encoding='utf-8', quotechar='"', engine='python')

    def parse_dt(x):
        match = re.search(r'\d{2}\.\d{2}\.\d{4}', str(x))
        return pd.to_datetime(match.group(), dayfirst=True) if match else pd.NaT

    df['reg_dt'] = df['termOfInitualRegistration'].apply(parse_dt)
    df['exp_dt'] = df['expirationDate'].apply(parse_dt)
    df['updates_count'] = df['dateAndNumberTheInclusionDecision'].str.count('від').fillna(0)
    df['lifespan_years'] = (df['exp_dt'] - df['reg_dt']).dt.days / 365.25

    print("\nФІНАЛЬНИЙ ЗВІТ ПО АНАЛІЗУ ГІПОТЕЗ ДРРРО")

    print("\nГіпотеза 1")
    df['activity_group'] = df['updates_count'].apply(
        lambda x: 'Висока активність (>5)' if x > 5 else 'Низька активність (<=5)')
    res_h1 = df.groupby('activity_group')['lifespan_years'].mean().round(2)

    print("-" * 50)
    print(f"{'Рівень активності моделі':<30} | {'Сер. термін (роки)':<15}")
    print("-" * 50)
    for group, val in res_h1.items():
        print(f"{group:<30} | {val:<15}")

    print("\nГіпотеза 2")
    top_applicants = df['applicant'].value_counts().head(5).index
    res_h2 = df[df['applicant'].isin(top_applicants)].groupby('applicant')['updates_count'].mean().sort_values(
        ascending=False).round(2)

    print("-" * 75)
    print(f"{'Компанія-заявник (назва та ЄДРПОУ)':<55} | {'Сер. оновлень':<15}")
    print("-" * 75)
    for name, val in res_h2.items():
        clean_name = name.replace('\n', ' ').strip()
        print(f"{clean_name[:53]:<55} | {val:<15}")

    print("\nГіпотеза 3")
    total_models = len(df)
    top_3_count = df['manufacturer'].value_counts().head(3).sum()
    share = (top_3_count / total_models) * 100

    print(f"Загальна кількість моделей: {total_models}")
    print(f"Моделей від ТОП-3 виробників: {top_3_count}")
    print(f"Частка ринку трьох найбільших заводів: {share:.1f}%")

if __name__ == "__main__":
    run_drrro_research()