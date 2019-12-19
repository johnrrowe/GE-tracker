import tkinter as tk
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def create_window(master, cursor, item):
    window = tk.Toplevel(master)

    # Query data
    item_data     = query_db(cursor, item)
    time          = item_data['time']
    buy_quantity  = item_data['buy_quantity']
    sell_quantity = item_data['sell_quantity']
    buy_price_data, sell_price_data = trim_prices(item_data)

    # Create plots and plot data
    Fig   = Figure(figsize=(12,4))
    plot1 = Fig.add_subplot(211)
    plot2 = Fig.add_subplot(212)

    plot1.plot(time, buy_quantity)
    plot1.plot(time, sell_quantity)
    plot1.legend(['Buy Quantity', 'Sell Quantity'])
    plot2.plot(buy_price_data[0], buy_price_data[1])
    plot2.plot(sell_price_data[0], sell_price_data[1])
    plot2.legend(['Buy Price', 'Sell Price'])

    # Draw plots to window
    canvas = FigureCanvasTkAgg(Fig, window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


def query_db(cursor, item):
    # Read data
    cursor.execute("SELECT * FROM "+item+';')
    header    = ['time', 'buy_price', 'buy_quantity', 'sell_price', 'sell_quantity']
    item_data = pd.DataFrame.from_records(cursor.fetchall(), columns=header)

    return item_data


def trim_prices(data):
    '''
    This function removes instances from price data where entries are 0.
    Prices are never really 0, and these instances occur when not enough items
    are being bought and sold. This also means price data need their own time vectors.
    '''

    buy_price  = [p for p in data['buy_price'] if p > 0]
    buy_time   = [data['time'][i] for i, p in enumerate(data['buy_price']) if p > 0]
    sell_price = [p for p in data['sell_price'] if p > 0]
    sell_time  = [data['time'][i] for i, p in enumerate(data['sell_price']) if p > 0]

    return (buy_time, buy_price), (sell_time, sell_price)
