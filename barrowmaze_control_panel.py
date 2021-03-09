import csv
import random
import re
import typing as T
from pathlib import Path
import codecs
from argparse import ArgumentParser
import tkinter as tk
from tkinter import messagebox

# pylint: disable=missing-class-docstring,missing-function-docstring,missing-module-docstring

def get_args():
    parser = ArgumentParser('barrowmaze_control_panel')
    parser.add_argument('--spoiler-safe', action='store_true')
    return parser.parse_args()


def parse_roll(formula: str) -> T.Optional[int]:
    scalar_match = re.fullmatch(r'([0-9]+)', formula)
    if scalar_match:
        return int(scalar_match.group(0))
    roll_match = re.match(r'([0-9]+)d([0-9]+)([+-][0-9]+)?', formula)
    if roll_match is not None:
        dice_count = int(roll_match.group(1))
        dice_type = int(roll_match.group(2))
        modifier = int(roll_match.group(3) or '0')
        return sum([random.randint(1, dice_type) for i in range(dice_count)]) + modifier
    return None


class Table:

    def __init__(self, path: str, spoiler_safe=False):
        self.path = path
        self.spoiler_safe = spoiler_safe
        content = list(csv.reader(open(path, 'r'), delimiter=';'))
        self.headers = [self.rot13(h) for h in content[0]]
        self.rows: T.List[T.Dict[str, str]] = [
            self.prepare_row(dict(zip(self.headers, row)))
            for row in content[1:]
        ]

    def prepare_row(self, row: dict) -> dict:
        dst = row.copy()
        for key in row:
            if row[key] == '':
                del dst[key]
            if key in ['HP', 'AMOUNT'] and key in dst:
                dst[key] = self.rot13(dst[key])
            if key == 'NEXT' and 'NEXT' in dst:
                dst[key] = [self.rot13(tn) for tn in dst[key].split(' ')]
        return dst

    def is_monster_table(self) -> bool:
        return 'HP' in self.headers

    def is_junction_table(self) -> bool:
        return 'NEXT' in self.headers

    def roll(self) -> dict:
        idx = random.randint(0, len(self.rows)-1)
        return self.rows[idx]

    def rot13(self, text: str) -> str:
        return codecs.encode(text, 'rot13') if self.spoiler_safe else text


class ControlPanel:

    def __init__(self, spoiler_safe):
        self.root = tk.Tk()
        self.root.geometry('400x300')
        self.root.wm_title('Barrowmaze Control Panel')

        self.spoiler_safe = spoiler_safe

        self.tables: T.Dict[Table] = dict()
        self.tablepath = Path('./tables/rot13' if self.spoiler_safe else './tables')
        for path in self.tablepath.glob('*.csv'):
            self.tables[path.stem] = Table(str(path), spoiler_safe=self.spoiler_safe)

        self.control_frame = tk.Frame(self.root, relief=tk.RAISED, borderwidth=1, padx=2, pady=2)
        self.control_frame.pack(padx=5, pady=5, ipadx=2, fill=tk.X)

        tk.Label(self.control_frame, text='Party Level').pack(side=tk.LEFT)
        self.player_level = tk.Spinbox(self.control_frame, from_=1, to=10, width=4)
        self.player_level.pack(side=tk.LEFT)

        self.generate_btn = tk.Button(
            self.control_frame,
            text='Restock room',
            command=self.restock_room
        )
        self.generate_btn.pack(side=tk.RIGHT)

        self.output = tk.Label(
            self.root,
            text='While the adventureres are away the skellies will play...',
            justify=tk.LEFT,
            relief=tk.SUNKEN,
            anchor=tk.NW,
            padx=5,
            pady=5,
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5, ipadx=5, ipady=5)

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
            amount = None
            if 'AMOUNT' in row:
                amount = parse_roll(row['AMOUNT'])
                ret += 'amount: {}\n'.format(amount or row['AMOUNT'])
            if 'HP' in row:
                amount = amount or 1
                ret += 'hp roll: {}\n'.format(row['HP'])
                if amount is not None and parse_roll(row['HP']) is not None:
                    hps = [
                        str(parse_roll(row['HP'])) or '| Weird error, ask Isak |'
                        for i in range(amount)
                    ]
                    ret += 'hitpoints: {}\n'.format(', '.join(hps))
            ret += '_'*80 + '\n'
            if 'NEXT' in row:
                for nextname in row['NEXT']:
                    ret += self.roll_traverse_table(nextname)
        else:
            ret += f'no table called "{table_name}"\n'
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
    args = get_args()
    app = ControlPanel(spoiler_safe=args.spoiler_safe)
    app.run()
