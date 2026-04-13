import pandas as pd
from pathlib import Path
import re
import warnings
import sqlite3

warnings.filterwarnings('ignore')

def run_drrro_research():

    DB_PATH = Path("/app/data/database.sqlite")

    RESULT_PATH = Path("/app/reports/research_results.txt")
    RESULT_PATH.parent.mkdir(exist_ok=True, parents=True)

    if not DB_PATH.exists():
        print(f"Базу даних не знайдено: {DB_PATH}")
        return


    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM rro_data", conn)
    conn.close()

    def parse_dt(x):
        match = re.search(r'\d{2}\.\d{2}\.\d{4}', str(x))
        return pd.to_datetime(match.group(), dayfirst=True) if match else pd.NaT

    df['reg_dt'] = df['termOfInitualRegistration'].apply(parse_dt)
    df['exp_dt'] = df['expirationDate'].apply(parse_dt)
    df['updates_count'] = df['dateAndNumberTheInclusionDecision'].str.count('від').fillna(0)
    df['lifespan_years'] = (df['exp_dt'] - df['reg_dt']).dt.days / 365.25

    output = []
    output.append("ФІНАЛЬНИЙ ЗВІТ ПО АНАЛІЗУ ГІПОТЕЗ ДРРРО")

    output.append("\nГіпотеза 1")
    df['activity_group'] = df['updates_count'].apply(
        lambda x: 'Висока активність (>5)' if x > 5 else 'Низька активність (<=5)')
    res_h1 = df.groupby('activity_group')['lifespan_years'].mean().round(2)
    for group, val in res_h1.items():
        output.append(f"{group}: {val} років")

    output.append("\nГіпотеза 2")
    top_applicants = df['applicant'].value_counts().head(5).index
    res_h2 = df[df['applicant'].isin(top_applicants)].groupby('applicant')['updates_count'].mean().sort_values(
        ascending=False).round(2)
    for name, val in res_h2.items():
        clean_name = str(name).replace('\n', ' ').strip()[:50]

        output.append(f"{clean_name}: {val} оновлень")

    output.append("\nГіпотеза 3")
    total_models = len(df)
    top_3_count = df['manufacturer'].value_counts().head(3).sum()
    share = (top_3_count / total_models) * 100
    output.append(f"Частка ринку ТОП-3 виробників: {share:.1f}%")

    final_text = "\n".join(output)
    print(final_text)

    with open(RESULT_PATH, "w", encoding="utf-8") as f:
        f.write(final_text)


if __name__ == "__main__":
    run_drrro_research()