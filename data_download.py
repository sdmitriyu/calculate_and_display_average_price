import yfinance as yf
import pandas as pd
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)


def fetch_stock_data(ticker, start_date, end_date):
    """
    Получает исторические данные о ценах акций для указанного тикера и диапазона дат.

    :param ticker: Строка, тикер акции (например, 'AAPL').
    :param start_date: Строка, начальная дата в формате 'YYYY-MM-DD'.
    :param end_date: Строка, конечная дата в формате 'YYYY-MM-DD'.
    :return: DataFrame с историческими данными о ценах акций.
    """
    try:
        # Получение данных акций
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)

        # Проверка, получены ли данные
        if data.empty:
            logging.warning(f"Нет данных для тикера {ticker} в указанный диапазон дат.")
            return pd.DataFrame()  # Возвращаем пустой DataFrame

        return data
    except Exception as e:
        logging.error(f"Ошибка при получении данных для тикера {ticker}: {e}")
        return pd.DataFrame()  # Возвращаем пустой DataFrame в случае ошибки


def add_moving_average(data, window_size=5):
    """
    Добавляет столбец со скользящей средней к DataFrame.

    :param data: DataFrame с данными акций.
    :param window_size: Размер окна для расчета скользящей средней.
    :return: DataFrame с добавленным столбцом 'Moving_Average'.
    """
    if 'Close' in data.columns:  # Проверяем, есть ли столбец 'Close'
        data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
        return data
    else:
        logging.error("Столбец 'Close' отсутствует в предоставленных данных.")
        return data  # Возвращаем исходный DataFrame без изменений


# Пример использования функций
if __name__ == "__main__":
    ticker = input("Введите тикер акции (например, 'AAPL'): ")
    start_date = input("Введите дату начала (YYYY-MM-DD): ")
    end_date = input("Введите дату окончания (YYYY-MM-DD): ")

    stock_data = fetch_stock_data(ticker, start_date, end_date)

    if not stock_data.empty:
        stock_data = add_moving_average(stock_data)
        print(stock_data.head())  # Выводим первые строки данных
