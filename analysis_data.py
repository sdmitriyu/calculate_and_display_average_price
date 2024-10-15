import logging
import pandas as pd


def calculate_and_display_average_price(stock_data):
    # Проверяем, что входной параметр — это DataFrame
    if not isinstance(stock_data, pd.DataFrame):
        logging.info("Ошибка: предоставленные данные не являются DataFrame.")
        print("Ошибка: предоставленные данные не являются DataFrame.")
        return

    # Проверяем, что в DataFrame есть столбец 'Close'
    if 'Close' not in stock_data.columns:
        logging.info("Ошибка: в DataFrame отсутствует столбец 'Close'.")
        print("Ошибка: в DataFrame отсутствует столбец 'Close'.")
        return

    # Вычисляем среднюю цену закрытия
    average_price = stock_data['Close'].mean()
    if pd.isna(average_price):
        print("Средняя цена закрытия за заданный период: недоступна (nan)")
    else:
        print(f"Средняя цена закрытия за заданный период: {average_price}")


def notify_if_strong_fluctuations(data, threshold):
    """
    Параметры:
        data (DataFrame): Данные акций, ожидается, что это DataFrame.
        threshold (float): Порог в процентах для проверки колебаний.
    Уведомление:
        Печатает сообщение о сильных колебаниях, если разница между максимальной и минимальной ценой превышает порог.
    """
    # Проверяем, что данные корректны
    if not isinstance(data, pd.DataFrame) or data.empty or 'Close' not in data.columns:
        print("Нет данных для анализа.")
        return

    # Вычисляем максимальную и минимальную цену
    max_price = data['Close'].max()
    min_price = data['Close'].min()

    if pd.isna(max_price) or pd.isna(min_price):
        print("Нет данных о ценах для вычисления колебаний.")
        return

    fluctuation = ((max_price - min_price) / min_price) * 100
    if fluctuation > threshold:
        print(f"Внимание: Цена акций колебалась более чем на {threshold}% за период.")
        print(f"Максимальная цена: {max_price}")
        print(f"Минимальная цена: {min_price}")
        print(f"Колебание: {fluctuation:.2f} %")
    else:
        print(f"Колебания цены акций не превышают {threshold}%.")
        print(f"Максимальная цена: {max_price}")
        print(f"Минимальная цена: {min_price}")
        print(f"Колебание: {fluctuation:.2f} %")


def export_data_to_csv(data, filename):
    """ Экспортирует данные об акциях в CSV файл. """
    try:
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Данные должны быть представлены в формате pandas DataFrame")
        data.to_csv(filename, index=False)
        print(f"Данные успешно экспортированы в файл {filename}")
    except Exception as e:
        print(f"Ошибка при экспорте данных: {e}")


def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    """ Вычисляет MACD для предоставленных данных акций. """
    if 'Close' not in data.columns:
        raise ValueError("Отсутствует столбец 'Close' в данных")

    short_ema = data['Close'].ewm(span=short_window, adjust=False).mean()
    long_ema = data['Close'].ewm(span=long_window, adjust=False).mean()
    data['MACD'] = short_ema - long_ema
    data['Signal'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    return data


def calculate_statistics(data):
    """
    Adds a statistical column representing the standard deviation of the closing price.

    Parameters:
    - data: DataFrame containing stock information with a 'Close' price column.

    Returns:
    - DataFrame with an additional column for standard deviation.
    """
    data['Close_std'] = data['Close'].rolling(window=30).std()
    return data
