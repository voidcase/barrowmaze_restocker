# pylint: disable=missing-class-docstring,missing-function-docstring,missing-module-docstring
import csv
import re
import random
import codecs
import typing as T
from pathlib import Path


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


def rot13(text: str) -> str:
    return codecs.encode(text, 'rot13')


class Restocker():

    def __init__(self, table_dir, spoiler_safe=False):
        self.tables: T.Dict[Table] = dict()
        self.tablepath = Path(table_dir)
        self.spoiler_safe = spoiler_safe
        for path in self.tablepath.glob('*.csv'):
            self.tables[path.stem] = Table(str(path), spoiler_safe=self.spoiler_safe)

    def roll_traverse_table(self, table_name='base', party_level=None):
        ret = ''
        if '_lvl' in table_name:
            table_name = table_name.replace('_lvl', '_{}'.format(
                self.get_level_interval(party_level, ['1-3', '4-6', '7-10'])
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
                    ret += self.roll_traverse_table(nextname, party_level=party_level)
        else:
            error_msg = f'no table called "{table_name}".'
            print(error_msg)
            ret += error_msg + '\n'
        return ret

    def get_level_interval(self, lvl, intervals: T.List[str]) -> T.Optional[str]:
        for interval in intervals:
            match = re.match(r'([0-9]+)-([0-9]+)', interval)
            if match is None:
                raise RuntimeError(
                    f'"{interval}" is not a level range.'
                )
            from_lvl = int(match.group(1))
            to_lvl = int(match.group(2))
            if from_lvl <= lvl <= to_lvl:
                return interval
        raise RuntimeError('Level is not in any range.')


class Table:

    def __init__(self, path: str, spoiler_safe=False):
        self.path = path
        self.spoiler_safe = spoiler_safe
        content = list(csv.reader(open(path, 'r'), delimiter=';'))
        self.headers = [rot13(h) for h in content[0]]
        self.rows: T.List[T.Dict[str, str]] = [
            self.prepare_row(dict(zip(self.headers, row)))
            for row in content[1:]
        ]

    def prepare_row(self, row: dict) -> dict:
        dst = row.copy()
        for key in row:
            if dst[key] == '':
                del dst[key]
        for key in dst:
            if key in ['HP', 'AMOUNT', 'NEXT'] or not self.spoiler_safe:
                # decipher non-spoiler-sensitive fields
                dst[key] = rot13(dst[key])
            if key == 'NEXT':
                dst[key] = dst[key].split(' ')
        return dst

    def is_monster_table(self) -> bool:
        return 'HP' in self.headers

    def is_junction_table(self) -> bool:
        return 'NEXT' in self.headers

    def roll(self) -> dict:
        idx = random.randint(0, len(self.rows)-1)
        return self.rows[idx]
