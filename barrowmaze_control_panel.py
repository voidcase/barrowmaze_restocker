# pylint: disable=missing-class-docstring,missing-function-docstring,missing-module-docstring
from argparse import ArgumentParser
import tkinter as tk
from tkinter import messagebox
from restocker import Restocker


def get_args():
    parser = ArgumentParser('barrowmaze_control_panel')
    parser.add_argument(
        '--spoiler-safe',
        '-s',
        action='store_true',
        help='all text from tables is in rot13'
    )
    return parser.parse_args()


class ControlPanel:

    def __init__(self, spoiler_safe):
        self.restocker = Restocker('./tables', spoiler_safe=spoiler_safe)
        self.root = tk.Tk()
        self.root.geometry('400x300')
        self.root.wm_title('Barrowmaze Control Panel')

        self.control_frame = tk.Frame(self.root, relief=tk.RAISED, borderwidth=1, padx=2, pady=2)
        self.control_frame.pack(padx=5, pady=5, ipadx=2, fill=tk.X)

        tk.Label(self.control_frame, text='Party Level').pack(side=tk.LEFT)
        self.party_level = tk.Spinbox(self.control_frame, from_=1, to=10, width=4)
        self.party_level.pack(side=tk.LEFT)

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
        try:
            text = self.restocker.roll_traverse_table(
                'base',
                party_level=int(self.party_level.get())
            )
            self.output.configure(text=text)
        except RuntimeError as err:
            messagebox.showerror('error', err)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    args = get_args()
    app = ControlPanel(spoiler_safe=args.spoiler_safe)
    app.run()
