from dearpygui.dearpygui import *


class Application(object):
    def __init__(self):
        self.show = True

    def update(self):
        add_window('title', 800, 600, 50, 50,
                   True, True, True,
                   True)
        add_table("Table##widget", ["Column 1", "Column 2", "Column 3", "Column 4"])

        tabledata = []
        for i in range(0, 10):
            row = []
            for j in range(0, 4):
                row.append("Item" + str(i) + "-" + str(j))
            tabledata.append(row)

        set_value("Table##widget", tabledata)
        start_dearpygui()


