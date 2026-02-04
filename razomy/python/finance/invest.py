def compound_interest_detailed():
    print("--- Детальный расчет сложного процента ---")

    try:
        # Ввод данных (по умолчанию 10 долларов, 10% годовых, 30 лет)
        principal_input = input("Стартовая сумма (Enter для 10): ")
        rate_input = input("Годовой процент % (Enter для 10%): ")
        years_input = input("Срок в годах (Enter для 30): ")

        principal = float(principal_input) if principal_input else 10.0
        rate = float(rate_input) if rate_input else 10.0
        years = int(years_input) if years_input else 30

        print(f"\nВклад: ${principal}")
        print(f"Ставка: {rate}% (с реинвестированием раз в год)")
        print(f"Срок: {years} лет\n")

        # Заголовок таблицы
        print(f"{'Год':<5} | {'Сумма ($)':<12} | {'Прибыль ($)':<12} | {'Рост (%)':<10}")
        print("-" * 46)

        current_amount = principal

        for year in range(1, years + 1):
            # Формула: Старая сумма + (Старая сумма * процент)
            # Мы используем это в цикле, чтобы видеть процесс год за годом
            current_amount = current_amount * (1 + rate / 100)

            # Чистая прибыль (текущая сумма - то, что вложили вначале)
            profit = current_amount - principal

            # Процент роста (на сколько % вырос начальный депозит)
            total_growth_percent = (profit / principal) * 100

            print(f"{year:<5} | {current_amount:<12.2f} | {profit:<12.2f} | +{total_growth_percent:<8.1f}%")

    except ValueError:
        print("Ошибка: вводите только числа.")


if __name__ == "__main__":
    compound_interest_detailed()