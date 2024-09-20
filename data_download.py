import yfinance as yf


# Получает исторические данные об акциях для указанного тикера и временного периода.md
# Возвращает DataFrame с данными.md
def fetch_stock_data(ticker, period='1mo'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


def add_moving_average(data, window_size=5):
    data = data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data

