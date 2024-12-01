from pathlib import Path
import numpy as np
import polars as pl
import os

class Day01():
    def __init__(self):
        input_file = Path(__file__).parent / 'input.txt'
        with open(input_file, 'rt') as in_f:
            self.input_lines = in_f.readlines()

    def __repr__(self):
        # return '\n'.join(self.input_lines)
        return '\n'.join(self.lists)
    
    def test_print(self):
        print(self.lists_df)
    
    def extract(self):
        self.lists_df = pl.DataFrame([
            np.sort(np.array([line.split()[0] for line in self.input_lines], dtype=np.int32)),
            np.sort(np.array([line.split()[1] for line in self.input_lines], dtype=np.int32))
        ])

    def transform(self):
        self.lists_df = self.lists_df.with_columns(
            (abs(pl.col('column_1') - pl.col('column_0'))) \
            .alias("col_diff")
        )

    def load(self):
        print(self.lists_df['col_diff'].sum())
        

day_01 = Day01()

day_01.extract()
day_01.transform()
day_01.load()

# print(day_01)
# day_01.test_print()