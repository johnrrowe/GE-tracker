from tkinter import *
import pandas as pd
import requests


class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        # Fetch item summary from OS Buddy Database
        summary = requests.get("https://rsbuddy.com/exchange/summary.json").json()
        keys = list(summary.keys())
        # Read in buy limits
        self.buy_limits = pd.read_csv("Buying_Limits.csv", index_col="Item")

        # Generate item table
        self.items = []
        for key in keys:
            name = summary[key]["name"]
            id = str(summary[key]["id"])

            try:
                self.items.append("{:<38s}{:<8s}{:d}".format(name, id, self.buy_limits.loc[name, "Buy limit"]))
            except:
                self.items.append("{:<38s}{:s}".format(name, id))


        self.pack()
        self.create_widgets()




    # Create main GUI window
    def create_widgets(self):
        self.windows = [self.master]
        self.search_var = StringVar()
        self.search_var.trace("w", lambda name, index, mode: self.update_list())
        self.entry = Entry(self, textvariable=self.search_var, width=35)
        self.item_table = Listbox(self, width=60, height=23, font = ('Courier',12))
        self.header = Listbox(self, width=60, height=1, font = ('Courier',12))
        self.header.insert(END, "{:<38s}{:<8s}{:s}".format("Item", "ID", "Buy Limit"))
        self.selectButton = Button(self, text='Select', underline = 0, command=self.selection)

        self.item_table.bind('<Double-1>', lambda x: self.selectButton.invoke())
        self.master.bind('<Escape>', lambda x: self.windows.pop().destroy())

        self.entry.grid(row=0, column=0, padx=10, pady=3)
        self.header.grid(row=1, column=0, padx=10, pady=3)
        self.item_table.grid(row=2, column=0, padx=10, pady=3)

        # Update list based on search entry -- needs to be called here to populate the listbox.
        self.update_list()



    def selection(self):
        dictionary = {"Cannonball" : self.cannonTest}

        try:
            dictionary[self.item_table.selection_get().split()[0]]()
        except:
            pass



    def cannonTest(self):
        print("Selected cannonball.")
        window = Toplevel(self.master)
        self.windows.append(window.master)


    def update_list(self):
        search_term = self.search_var.get()
        # List of items to search from
        item_table_list = self.items
        # Delete items in listbox
        self.item_table.delete(0, END)
        # Add items that begin with search_term -- not case sensitive
        for item in item_table_list:
            if search_term.lower() in item.lower():
                self.item_table.insert(END, item)





root = Tk()
root.title('Filter Listbox Test')
app = Application(master=root)
app.mainloop()
