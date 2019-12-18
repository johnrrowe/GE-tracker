import tkinter as tk
import requests
from pandas import read_csv
from db_connector import connect_to_db
import plotter


class Application(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        # MySQL database connection
        self.conn, self.cursor = connect_to_db()

        # Fetch item summary from OS Buddy Database
        summary = requests.get("https://rsbuddy.com/exchange/summary.json").json()
        keys    = list(summary.keys())
        # Read in buy limits
        self.buy_limits = read_csv("Buying_Limits.csv", index_col="Item")

        # Generate item table data
        self.items = []
        for key in keys:
            name = summary[key]["name"]
            id   = str(summary[key]["id"])
            try:
                self.items.append.tk.END("{:<38s}{:<8s}{:d}".format(name, id, self.buy_limits.loc[name, "Buy limit"]))
            except:
                self.items.append("{:<38s}{:s}".format(name, id))

        self.pack()
        self.create_widgets()


    def __del__(self):
        # Close out database connection
        self.cursor.close()
        self.conn.close()
        print("Connection closed.")


    # Create main GUI window
    def create_widgets(self):
        # gui properties that need to be called outside of create_widgets()
        self.item_table  = tk.Listbox(self, width=60, height=23, font = ('Courier',12))
        self.search_term = tk.StringVar()
        self.search_term.trace("w", lambda name, index, mode: self.update_list())

        # gui properties that DO NOT need to be called outside of create_widgets()
        search_bar   = tk.Entry(self, textvariable=self.search_term, width=35)
        selectButton = tk.Button(self, text='Select', underline = 0, command=self.open_graph)
        header       = tk.Listbox(self, width=60, height=1, font = ('Courier',12))
        header.insert(tk.END, "{:<38s}{:<8s}{:s}".format("Item", "ID", "Buy Limit"))

        # Display elements in the window
        search_bar.grid(row=0, column=0, padx=10, pady=3)
        header.grid(row=1, column=0, padx=10, pady=3)
        self.item_table.grid(row=2, column=0, padx=10, pady=3)

        # KEY BINDINGS
        self.item_table.bind('<Double-1>', lambda x: selectButton.invoke())
        self.master.bind('<Escape>', lambda x: self.master.destroy())

        # Filter list based on the search_bar entry -- needs to be called here to populate the listbox.
        self.update_list()



    def open_graph(self):
        # Ignore the first 38 characters of the selection then grab the id
        ITEM_SPACING = 38
        ID = self.item_table.selection_get()[ITEM_SPACING:].split()[0]

        plotter.create_window(self.master, self.cursor, "item"+ID)



    def update_list(self):
        search_term = self.search_term.get()
        # List of items to search from
        item_table_list = self.items
        # Delete items in listbox
        self.item_table.delete(0, tk.END)
        # Add items that begin with search_term -- not case sensitive
        for item in item_table_list:
            if search_term.lower() in item.lower():
                self.item_table.insert(tk.END, item)





root = tk.Tk()
root.title('Filter Listbox Test')
app = Application(master=root)
app.mainloop()
