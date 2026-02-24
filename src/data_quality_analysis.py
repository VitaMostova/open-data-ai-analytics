import pandas as pd
from pathlib import Path


def analyze_drrro_quality():
    BASE_DIR = Path(__file__).resolve().parents[1]
    raw_path = BASE_DIR / "data" / "raw" / "drrro.csv"
    report_path = BASE_DIR / "reports" / "data_quality_report.md"
    report_path.parent.mkdir(exist_ok=True, parents=True)

    if not raw_path.exists():
        print(f"Файл не знайдено: {raw_path}")
        return


    df = pd.read_csv(raw_path, sep=';', encoding='utf-8', quotechar='"', engine='python')

    report = ["# Розширений звіт про якість даних ДРРРО\n"]


    report.append("## 1. Структура датасету")
    report.append(f"- **Кількість моделей РРО:** {len(df)}")
    report.append(f"- **Кількість ознак:** {len(df.columns)}\n")

    stats_table = "| Колонка | Заповненість | Унікальних значень | Тип даних |\n|---|---|---|---|"
    for col in df.columns:
        non_null = df[col].notnull().sum()
        unique = df[col].nunique()
        dtype = "Текст/Об'єкт"
        stats_table += f"\n| {col} | {non_null}/{len(df)} | {unique} | {dtype} |"
    report.append(stats_table)


    report.append("\n## 2. Аналіз ключових полів")


    top_manufacturers = df['manufacturer'].value_counts().head(3)
    report.append("### Виробники та заявники")
    report.append(
        f"- Найбільший виробник: `{top_manufacturers.index[0].splitlines()[0]}` ({top_manufacturers.values[0]} моделей)")


    software_issues = df['softwareVersion'].str.contains('\n').sum()
    report.append(f"- Кількість моделей з кількома версіями ПЗ: {software_issues}")


    report.append("\n## 3. Валідація складних форматів")

    def parse_complex_date(x):
        if pd.isna(x): return "Пропуск"

        import re
        match = re.search(r'\d{2}\.\d{2}\.\d{4}', str(x))
        return "OK" if match else "Невірний формат"

    df['reg_status'] = df['termOfInitualRegistration'].apply(parse_complex_date)
    df['exp_status'] = df['expirationDate'].apply(parse_complex_date)

    report.append(f"- Коректність дат реєстрації: {df['reg_status'].value_counts().get('OK', 0)} з {len(df)}")
    report.append(f"- Коректність дат виведення: {df['exp_status'].value_counts().get('OK', 0)} з {len(df)}")


    update_counts = df['dateAndNumberTheInclusionDecision'].str.count('від').fillna(0)
    report.append(f"- Середня кількість рішень (оновлень) на одну модель: {update_counts.mean():.1f}")
    report.append(f"- Максимальна кількість оновлень для моделі: {int(update_counts.max())}")


    report.append("\n## 4. Сфери застосування")

    all_scopes = df['scopeOfAplication'].str.replace('"', '').str.lower().str.split(';').explode().str.strip()
    scope_counts = all_scopes.value_counts().head(5)
    report.append("Найпопулярніші сфери:")
    for s, c in scope_counts.items():
        if s: report.append(f"- {s.capitalize()}: {c} моделей")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report))

    print(f"Детальний аналіз завершено. Звіт тут: {report_path}")


if __name__ == "__main__":
    analyze_drrro_quality()