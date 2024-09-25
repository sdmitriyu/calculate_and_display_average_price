import logging
import pandas as pd

def calculate_and_display_average_price(stock_data):
    # Проверяем, что входной параметр — это DataFrame
    if not isinstance(stock_data, pd.DataFrame):
        logging.INFO
        print("Ошибка: предоставленные данные не являются DataFrame.")
        return


    # Проверяем, что в DataFrame есть столбец 'Close'
    if 'Close' not in stock_data.columns:
        logging.INFO
        print("Ошибка: в DataFrame отсутствует столбец 'Close'.")
        return

    # Вычисляем среднюю цену закрытия
    average_price = stock_data['Close'].mean()

    # Выводим среднюю цену закрытия
    print(f"Средняя цена закрытия за заданный период: {average_price}")




def notify_if_strong_fluctuations(data, threshold):
    """
    Параметры:
        data (list): Список цен закрытия акций.
        threshold (float): Порог в процентах для проверки колебаний.

    Уведомление:
        Печатает сообщение о сильных колебаниях, если разница между максимальной и минимальной ценой превышает порог.
    """

    # if not data:
    #     print("Нет данных для анализа.")
    #     return

    max_price = max(data['Close'])
    min_price = min(data['Close'])
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
    """
    Экспортирует данные об акциях в CSV файл.

    :param data: DataFrame с данными об акциях
    :param filename: Имя файла, в который будут сохранены данные
    """
    try:
        # Проверяем, что данные представлены в формате DataFrame
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Данные должны быть представлены в формате pandas DataFrame")

        # Используем метод to_csv для сохранения данных в CSV файл
        data.to_csv(filename, index=False)
        print(f"Данные успешно экспортированы в файл {filename}")

    except Exception as e:
        print(f"Ошибка при экспорте данных: {e}")