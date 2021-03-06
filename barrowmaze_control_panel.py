import csv
import random
import re
import typing as T
import tkinter as tk
from tkinter import ttk



class ControlPanel:
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('600x200')
        self.root.wm_title('Barrowmaze Control Panel')

        self.txt = tk.Label(self.root, text='Hej Max')
        self.txt.pack()

        self.generate_btn = tk.Button(self.root, text='Restock room', command=self.restock_room)
        self.generate_btn.pack()

        player_level_label = tk.Label(self.root, text='Player Level')
        self.player_level = ttk.Combobox(self.root, values=[i for i in range(1, 20)])
        self.player_level.pack()

        

    def restock_room(self):
        self.txt.configure(text=self.get_level_interval(['1-3','4-6','7-9']))

    def get_level_interval(self, intervals: T.List[str]) -> T.Optional[str]:
        lvl = self.player_level.current() + 1
        print('lvl:', lvl)
        for interval in intervals:
            m = re.match(r'([0-9]+)-([0-9]+)', interval)
            from_lvl = int(m.group(1))
            to_lvl = int(m.group(2))
            if from_lvl <= lvl <= to_lvl:
                return interval
        return None

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = ControlPanel()
    app.run()
