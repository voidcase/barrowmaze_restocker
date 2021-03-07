import csv
import random
import re
import typing as T
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import codecs

# pylint: disable=missing-class-docstring,missing-function-docstring,missing-module-docstring

def rot13(text: str) -> str:
    return codecs.encode(text, 'rot13')


class Table:

    def __init__(self, path: str):
        self.path = path
        content = list(csv.reader(open(path, 'r'), delimiter=';'))
        self.headers = [rot13(h) for h in content[0]]
        self.rows: T.List[T.Dict[str, str]] = [
            self.prepare_row(dict(zip(self.headers, row)))
            for row in content[1:]
        ]

    def prepare_row(self, row: dict) -> dict:
        dst = row.copy()
        for key in row:
            if row[key] == '':
                del dst[key]
            if key == 'NEXT' and 'NEXT' in dst:
                dst[key] = [rot13(tn) for tn in dst[key].split(' ')]
        return dst

    def is_monster_table(self) -> bool:
        return 'HP' in self.headers

    def is_junction_table(self) -> bool:
        return 'NEXT' in self.headers

    def roll(self) -> dict:
        idx = random.randint(0, len(self.rows)-1)
        return self.rows[idx]


class ControlPanel:

    def __init__(self):
        self.tables: T.Dict[Table] = dict()
        self.tablepath = Path('./tables/rot13')
        for path in self.tablepath.glob('*.csv'):
            self.tables[path.stem] = Table(str(path))

        self.root = tk.Tk()
        self.root.geometry('450x400')
        self.root.wm_title('Barrowmaze Control Panel')
        
        self.control_frame = tk.Frame(self.root, relief=tk.RAISED, borderwidth=1)
        self.control_frame.pack(padx=5, pady=5, ipadx=2, fill=tk.X)

        self.player_level_label = tk.Label(self.control_frame, text='Party Level')
        self.player_level_label.pack(side=tk.LEFT)
        self.player_level = tk.Spinbox(self.control_frame, from_=1, to=10, width=4)
        self.player_level.pack(side=tk.LEFT)

        self.generate_btn = tk.Button(
            self.control_frame,
            text='Restock room',
            command=self.restock_room
        )
        self.generate_btn.pack(side=tk.RIGHT)

        self.output = tk.Label(self.root, text='hejmax')
        self.output.pack()

    def restock_room(self):
        text = self.roll_traverse_table('base')
        self.output.configure(text=text)

    def roll_traverse_table(self, table_name: str):
        ret = ''
        if '_lvl' in table_name:
            table_name = table_name.replace('_lvl', '_{}'.format(
                self.get_level_interval(['1-3', '4-6', '7-10'])
            ))
        if table_name in self.tables:
            table: Table = self.tables[table_name]
            row = table.roll()
            ret += '{}: {}\n'.format(table_name, row['NAME'])
            if 'AMOUNT' in row:
                ret += 'AMOUNT: {}\n'.format(row['AMOUNT'])
            if 'HP' in row:
                ret += 'HP: {}\n'.format(row['HP'])
            ret += '-'*10 + '\n'
            if 'NEXT' in row:
                for nextname in row['NEXT']:
                    ret += self.roll_traverse_table(nextname)
        else:
            ret += f'oi mate, cound not find a table called "{table_name}"\n'
        return ret

    def get_level_interval(self, intervals: T.List[str]) -> T.Optional[str]:
        lvl = int(self.player_level.get())
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
