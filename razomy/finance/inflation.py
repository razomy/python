import ssl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from fredapi import Fred

# 1. ФИКС ДЛЯ МАК (SSL)
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# 2. ВСТАВЬ СЮДА СВОЙ КЛЮЧ
API_KEY = ''


def analyze_inflation_percentage():
    print("--- Запуск анализа в процентах ---")

    if API_KEY == 'ВСТАВЬ_СЮДА_СВОЙ_КЛЮЧ' or not API_KEY:
        print("ОШИБКА: Ключ API не вставлен!")
        return

    try:
        fred = Fred(api_key=API_KEY)
        data = fred.get_series('CPIAUCSL', observation_start='1990-01-01')
    except Exception as e:
        print(f"Ошибка соединения с API: {e}")
        return

    # Создаем таблицу и чистим данные
    df = pd.DataFrame(data, columns=['CPI'])
    df.index.name = 'Date'
    df.dropna(inplace=True)  # Удаляем пустые значения

    # Фильтр: последние 30 лет
    start_date = datetime.now() - timedelta(days=30 * 365)
    df = df[df.index >= start_date]

    if df.empty:
        print("Нет данных.")
        return

    # === ПРЕВРАЩЕНИЕ В ПРОЦЕНТЫ ===
    # Берем самое первое значение (30 лет назад) за Базу
    base_cpi = df['CPI'].iloc[0]

    # Считаем процент прироста для каждой точки относительно старта
    # Формула: ((Текущее - Базовое) / Базовое) * 100
    df['CPI_Pct'] = ((df['CPI'] - base_cpi) / base_cpi) * 100

    # --- МАТЕМАТИКА ---
    df['Date_Ordinal'] = df.index.map(datetime.toordinal)
    X = df['Date_Ordinal'].values.reshape(-1, 1)

    # Теперь мы обучаем модель предсказывать ПРОЦЕНТЫ, а не индекс
    y = df['CPI_Pct'].values

    model = LinearRegression()
    model.fit(X, y)

    # Прогноз на 30 лет
    future_years = 30
    future_days = future_years * 365
    last_date_ordinal = X[-1][0]

    future_X = np.arange(last_date_ordinal, last_date_ordinal + future_days, 30).reshape(-1, 1)
    future_pred_pct = model.predict(future_X)  # Предсказанные проценты
    future_dates = [datetime.fromordinal(int(x)) for x in future_X.flatten()]

    # Статистика
    current_pct_growth = y[-1]  # На сколько % выросло за прошлые 30 лет
    future_pct_growth = future_pred_pct[-1]  # На сколько % вырастет через след. 30 лет (от базы)

    # Прирост только за следующие 30 лет (относительно сегодня)
    # Математика сложнее: (FutureIndex / CurrentIndex - 1) * 100
    # Восстанавливаем индексы для точного расчета
    current_index_val = base_cpi * (1 + current_pct_growth / 100)
    future_index_val = base_cpi * (1 + future_pct_growth / 100)
    future_growth_clean = ((future_index_val / current_index_val) - 1) * 100

    print("\n=== РЕЗУЛЬТАТЫ (Накопленная инфляция) ===")
    print(f"За ПОСЛЕДНИЕ 30 лет цены выросли на: +{current_pct_growth:.2f}%")
    print(f"По вектору тренда, за СЛЕДУЮЩИЕ 30 лет цены вырастут еще на: +{future_growth_clean:.2f}%")
    print("-" * 40)
    print(f"Общий рост за 60 лет (от начала графика до конца прогноза): +{future_pct_growth:.2f}%")

    # 5. УЛУЧШЕННЫЙ ГРАФИК
    fig, ax = plt.subplots(figsize=(14, 8))  # Сделали график побольше

    # Линия тренда
    ax.plot(df.index, model.predict(X), color='green', linestyle=':', alpha=0.6, label='Вектор тренда')

    # Рисуем основные линии
    ax.plot(df.index, y, label='Факт (Прошлые 30 лет)', color='#1f77b4', linewidth=2.5)
    ax.plot(future_dates, future_pred_pct, label='Прогноз (След. 30 лет)', color='#d62728', linestyle='--', linewidth=2)
    ax.plot(future_dates, future_pred_pct + 20, label='Прогноз (След. 30 лет)', color='#d62728', linestyle='--', linewidth=2)


    # --- ДОБАВЛЕНИЕ МЕТОК (LABEL) КАЖДЫЕ 5 ЛЕТ ---

    # Объединяем прошлое и будущее в один список, чтобы пройтись циклом
    all_dates = list(df.index) + future_dates
    all_values = list(y) + list(future_pred_pct)

    annotated_years = set()  # Чтобы не ставить несколько меток на один год

    for i, date in enumerate(all_dates):
        # Проверяем: если год делится на 5 (2000, 2005...) и мы его еще не рисовали
        if date.year % 5 == 0 and date.year not in annotated_years:
            val = all_values[i]

            # 1. Рисуем черную точку на линии
            ax.scatter(date, val, color='black', s=40, zorder=5)

            # 2. Добавляем текст в рамочке
            ax.annotate(f"{val:.0f}%",
                        xy=(date, val),
                        xytext=(-5, 15),  # Сдвиг текста чуть вверх и влево
                        textcoords='offset points',
                        fontsize=9,
                        fontweight='bold',
                        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#b0b0b0", alpha=0.9))

            annotated_years.add(date.year)

    # --- НАСТРОЙКА СЕТКИ (GRID) ---

    # Включаем мелкие деления (minor ticks)
    ax.minorticks_on()

    # Основная сетка (по 10-20%) - сплошная линия
    ax.grid(which='major', linestyle='-', linewidth=0.8, color='gray', alpha=0.5)

    # Дополнительная сетка (помежуточная) - пунктирная линия
    ax.grid(which='minor', linestyle=':', linewidth=0.5, color='gray', alpha=0.3)

    # Форматирование оси Y (добавляем знак %)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())

    # Финальные штрихи
    plt.title('Инфляционный вектор: Детализация каждые 5 лет', fontsize=16)
    plt.ylabel('Накопленный рост цен (%)', fontsize=12)
    plt.xlabel('Год', fontsize=12)
    plt.legend(loc='upper left', fontsize=11, frameon=True, shadow=True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    analyze_inflation_percentage()