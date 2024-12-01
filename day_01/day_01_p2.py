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
        print(self.lists_joined)
    
    def extract(self):
        self.list_1, self.list_2 = \
            np.array([line.split()[0] for line in self.input_lines], dtype=np.int32), \
            np.array([line.split()[1] for line in self.input_lines], dtype=np.int32)
    
    @staticmethod
    def count_agg(input_list):
        list_agg = pl.DataFrame(input_list)
        # list_agg = list_agg.group_by('column_0').len()
        list_agg = list_agg.group_by('column_0').agg(
            pl.col('column_0').len().alias('num_count')
        ).select(
            pl.col("column_0").alias('num'),
            'num_count'
        )
        return list_agg

    def transform(self):
        self.lists_joined = self.count_agg(self.list_1).join(
            self.count_agg(self.list_2),
            on='num'
        ).select(
            'num',
            pl.col('num_count').alias('num_count_left'),
            'num_count_right'
        )

    def load(self):
        self.lists_quant = self.lists_joined.with_columns(
            ( pl.col('num') * pl.col('num_count_left') * pl.col('num_count_right') ). \
            alias('product')
        )
        # print(self.lists_quant)

        product_sum = self.lists_quant['product'].sum()
        print(f'{product_sum=}')

day_01 = Day01()

day_01.extract()
day_01.transform()
day_01.load()
# day_01.test_print()

