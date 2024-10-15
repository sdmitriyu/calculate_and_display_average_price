import yfinance as yf
import logging
import os
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# 1. Получение данных о тикере с помощью yfinance
def get_stock_data(ticker, start_date, end_date):
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        if stock_data.empty:
            logging.warning(f"Нет данных для тикера {ticker} в указанный диапазон дат.")
            return None
        stock_data.reset_index(inplace=True)
        if 'Date' not in stock_data.columns:
            logging.error(f"Колонка 'Date' отсутствует в данных: {stock_data.columns.tolist()}")
            raise KeyError("'Date' column is missing in the fetched stock data")
        return stock_data
    except Exception as e:
        logging.error(f"Ошибка при получении данных: {e}")
        return None


# 2. Создание статического графика с использованием matplotlib
def create_static_plot(data, ticker, period, style):
    try:
        plt.style.use(style)
        dates = data['Date']
        plt.figure(figsize=(10, 6))
        plt.plot(dates, data['Close'], label=f'{ticker} Close Price')
        plt.title(f'График цен закрытия {ticker} за {period}')
        plt.xlabel('Дата')
        plt.ylabel('Цена закрытия ($)')
        plt.legend()
        plt.grid()

        # Проверка на наличие индикаторов RSI и MACD для добавления на график
        if 'RSI' in data.columns:
            plt.figure(figsize=(10, 4))
            plt.plot(dates, data['RSI'], label='RSI', color='purple')
            plt.axhline(30, linestyle='--', alpha=0.5, color='red')
            plt.axhline(70, linestyle='--', alpha=0.5, color='green')
            plt.legend()
            plt.title('Индекс RSI')
            plt.grid()

        if 'MACD' in data.columns and 'Signal Line' in data.columns:
            plt.figure(figsize=(10, 4))
            plt.plot(dates, data['MACD'], label='MACD', color='blue')
            plt.plot(dates, data['Signal Line'], label='Сигнальная линия', color='red')
            plt.legend()
            plt.title('Индикатор MACD')
            plt.grid()

        # Сохранение графика в файл
        directory = "images"
        os.makedirs(directory, exist_ok=True)
        filename = os.path.join(directory, f"{ticker}_{period}_stock_price_chart.png")
        plt.savefig(filename)
        print(f"Статический график сохранен как {filename}!")

    except KeyError as e:
        logging.error(f"Ошибка доступа к данным: {e}. Проверьте, что колонка существует.")
    except Exception as e:
        logging.error(f"Ошибка при создании графика: {e}")
    finally:
        plt.close()


# Создание интерактивного графика с использованием plotly
def create_interactive_plot(data, ticker):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Close Price'))

    # Настройки графика
    fig.update_layout(
        title=f'Цены акций для {ticker}',
        xaxis_title='Дата',
        yaxis_title='Цена закрытия ($)',
        hovermode='x unified'
    )

    # Показ графика
    fig.show()


# Основная функция для выполнения всех задач
def main(stock_data, ticker, start_date, end_date, period, style):
    # Получение данных
    stock_data = get_stock_data(ticker, start_date, end_date)
    if stock_data is None:
        print(f"Не удалось получить данные для тикера {ticker}")
        return

    # Создание статического графика
    create_static_plot(stock_data, ticker, period, style)

    # Создание интерактивного графика
    create_interactive_plot(stock_data, ticker)

    # Сохранение данных в CSV файл
    csv_filename = f'{ticker}_stock_data.csv'
    stock_data.to_csv(csv_filename, index=False)
    print(f"Данные о акциях сохранены в {csv_filename}")
