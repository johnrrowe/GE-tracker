import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt


def create_window(master, cursor, item):
    window = tk.Toplevel(master)

    item_data = query_db(cursor, item)
    print(item_data.head())


def query_db(cursor, item):
    # Read data
    cursor.execute("SELECT * FROM "+item+';')
    header = ['time', 'buy_price', 'buy_quantity', 'sell_price', 'sell_quantity']
    item_data = pd.DataFrame.from_records(cursor.fetchall(), columns=header)

    return item_data
