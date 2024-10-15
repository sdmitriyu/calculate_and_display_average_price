import logging
import argparse
from datetime import datetime
import matplotlib.pyplot as plt
import data_download as dd
import data_plotting as dplt
import analysis_data as ad

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    filename='journal.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H-%M-%S'
)


def main(start_date: str = "2022-01-01", end_date: str = "2022-12-31"):
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print(
        "Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print(
        "Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")

    ticker = input("Введите тикер акции (например, 'AAPL' для Apple Inc): ")

    parser = argparse.ArgumentParser(description='Анализ данных о стоимости акций.')
    parser.add_argument('--start_date', type=str, help='Дата начала в формате ГГГГ-ММ-ДД', required=False)
    parser.add_argument('--end_date', type=str, help='Дата окончания в формате ГГГГ-ММ-ДД', required=False)

    args = parser.parse_args()

    if not args.start_date:
        start_date_input = input("Введите дату начала в формате ГГГГ-ММ-ДД (по умолчанию 2020-01-01): ")
        start_date = datetime.strptime(start_date_input, '%Y-%m-%d') if start_date_input else datetime(year=2020, month=1, day=1)
    else:
        start_date = datetime.strptime(args.start_date, '%Y-%m-%d')

    if not args.end_date:
        end_date_input = input("Введите дату окончания в формате ГГГГ-ММ-ДД (по умолчанию текущая дата): ")
        end_date = datetime.strptime(end_date_input, '%Y-%m-%d') if end_date_input else datetime.now()
    else:
        end_date = datetime.strptime(args.end_date, __format='%Y-%m-%d')

    period = end_date - start_date

    # Предполагаем, что функция fetch_stock_data возвращает датафрейм с колонкой 'Date'
    stock_data = dd.fetch_stock_data(ticker, start_date, end_date)
    print(stock_data.head())
    print(stock_data.columns)

    ad.calculate_and_display_average_price(stock_data)
    threshold = 30
    ad.notify_if_strong_fluctuations(stock_data, threshold)

    filename = "Information_about_promotions.csv"
    ad.export_data_to_csv(stock_data, filename)

    ad.calculate_macd(stock_data)
    stock_data = dd.add_moving_average(stock_data)
    ad.calculate_statistics(stock_data)

    # Выбор стиля оформления графиков
    available_styles = plt.style.available
    print("Доступные стили:", available_styles)
    user_style = input("Выберите стиль графика (например, 'ggplot', 'seaborn', 'classic'): ")
    if user_style not in available_styles:
        print(f"Стиль '{user_style}' недоступен. Используется стиль 'default'.")
        user_style = 'default'

    # Указание имени файла для сохранения графика
    plot_filename = f"{ticker}_{period.days}_days_stock_price_chart.png"
    dplt.main(stock_data, ticker, start_date, end_date, period, user_style)


if __name__ == "__main__":
    main()
