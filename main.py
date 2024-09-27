import data_download as dd
import data_plotting as dplt
import logging
import analisis_data as ad

logging.basicConfig(level=logging.DEBUG, filename='journal.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print("Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc):»")
    period = input("Введите период для данных (например, '1mo' для одного месяца): ")

    # Получает данные о запасах
    stock_data = dd.fetch_stock_data(ticker, period)

    # Проверяет, лигетивен ли DataFrame, и выводит из него среднюю цену закрытия акции
    ad.calculate_and_display_average_price(stock_data)

    threshold = 30

    # Анализирует данные и уведомляет пользователя, если цена акций колебалась более чем на заданный процент за период.
    ad.notify_if_strong_fluctuations(stock_data, threshold)

    filename = "Information_about_promotions"

    # Экспортирует данные в CSV файл.
    ad.export_data_to_csv(stock_data, filename)

    # Добавляет дополнительные технические индикаторы
    ad.calculate_macd(stock_data)

    # Добавляет скользящее среднее значение к данным
    stock_data = dd.add_moving_average(stock_data)

    # Строит график данных
    dplt.create_and_save_plot(stock_data, ticker, period)


if __name__ == "__main__":
    main()


