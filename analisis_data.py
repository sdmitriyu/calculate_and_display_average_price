def calculate_and_display_average_price(stock_data):
    # Проверяем, что входной параметр — это DataFrame
    if not isinstance(data, pd.DataFrame):
        print("Ошибка: предоставленные данные не являются DataFrame.")
        return

    # Проверяем, что в DataFrame есть столбец 'Close'
    if 'Close' not in stock_data.columns:
        print("Ошибка: в DataFrame отсутствует столбец 'Close'.")
        return

    # Вычисляем среднюю цену закрытия
    average_price = stock_data['Close'].mean()

    # Выводим среднюю цену закрытия
    print(f"Средняя цена закрытия за заданный период: {average_price}")
