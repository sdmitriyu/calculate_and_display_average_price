import matplotlib.pyplot as plt
import pandas as pd

def create_and_save_plot(data, ticker, period, style='default', filename=None):
    """
    Создает и сохраняет график цен, RSI и MACD с заданным стилем оформления.

    :param data: Данные для построения графиков. Ожидается DataFrame.
    :param ticker: Тикер акции.
    :param period: Период данных.
    :param style: Стиль оформления графиков. По умолчанию 'default'.
    :param filename: Имя файла для сохранения графика. Если не указано, будет создано автоматически.
    """
    plt.style.use(style)
    plt.figure(figsize=(10, 18))  # Увеличенное полотно для трех графиков

    # График цен
    plt.subplot(3, 1, 1)  # Первый график
    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            plt.plot(dates, data['Close'].values, label='Close Price')
            plt.plot(dates, data['Moving_Average'].values, label='Moving Average')
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.plot(data['Date'], data['Close'], label='Close Price')
        plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')

    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    # График RSI
    if 'RSI' in data.columns:
        plt.subplot(3, 1, 2)  # Второй график
        plt.plot(data['Date'] if 'Date' in data else data.index, data['RSI'], label='RSI', color='purple')
        plt.axhline(30, linestyle='--', alpha=0.5, color='red')
        plt.axhline(70, linestyle='--', alpha=0.5, color='green')
        plt.title('RSI')
        plt.legend()
    else:
        print("Колонка 'RSI' отсутствует в данных.")

    # График MACD
    if 'MACD' in data.columns and 'Signal Line' in data.columns:
        plt.subplot(3, 1, 3)  # Третий график
        plt.plot(data['Date'] if 'Date' in data else data.index, data['MACD'], label='MACD', color='blue')
        plt.plot(data['Date'] if 'Date' in data else data.index, data['Signal Line'], label='Signal Line', color='red')
        plt.title('MACD')
        plt.legend()
    else:
        print("Колонки 'MACD' или 'Signal Line' отсутствуют в данных.")

    # Сохранение файла
    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"
    plt.savefig(filename)
    plt.close()
    print(f"График сохранен как {filename}")


