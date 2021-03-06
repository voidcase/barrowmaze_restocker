import csv
import random
import re
import typing as T
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# pylint: disable=missing-class-docstring,missing-function-docstring


class Table:

    def __init__(self, path: str):
        self.path = path
        content = list(csv.reader(open(path, 'r')))
        self.headers = content[0]
        self.rows: T.List[T.Dict[str, str]] = [
            dict(zip(self.headers, row))
            for row in content[1:]
        ]

    def is_monster_table(self) -> bool:
        return 'HP' in self.headers

    def is_junction_table(self) -> bool:
        return 'NEXT' in self.headers

    def roll(self) -> dict:
        idx = random.randint(0, len(self.rows))
        return self.rows[idx]


class ControlPanel:

    def __init__(self):
        self.tables: T.Dict[Table] = dict()
        self.tablepath = Path('./tables')
        for path in self.tablepath.glob('*.csv'):
            self.tables[path.stem] = Table(str(path))

        self.root = tk.Tk()
        self.root.geometry('600x200')
        self.root.wm_title('Barrowmaze Control Panel')

        self.txt = tk.Label(self.root, text='Hej Max')
        self.txt.pack()

        self.generate_btn = tk.Button(self.root, text='Restock room', command=self.restock_room)
        self.generate_btn.pack()

        self.player_level = ttk.Combobox(self.root, values=list(range(1, 20)))
        self.player_level.pack()

    def restock_room(self):
        self.txt.configure(text=self.get_level_interval(['1-3','4-6','7-9']))
        base = self.tables['base']
        outcome = base.roll()

    def get_level_interval(self, intervals: T.List[str]) -> T.Optional[str]:
        lvl = self.player_level.current() + 1
        print('lvl:', lvl)
        for interval in intervals:
            match = re.match(r'([0-9]+)-([0-9]+)', interval)
            if match is None:
                messagebox.showerror(
                    'bad level range',
                    f'"{interval}" is not a level range. Ask Isak.'
                )
                return None
            from_lvl = int(match.group(1))
            to_lvl = int(match.group(2))
            if from_lvl <= lvl <= to_lvl:
                return interval
        return None

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = ControlPanel()
    app.run()