
'''
Shamelessly cheesing Part 2 with string .split().
'''

import sys, re
from math import prod

with open(sys.argv[1], 'r') as file:
    inp = file.read()

def extract_sum(data):
    return sum(map(prod, [map(int,m) for m in re.findall("mul\((\d+),(\d+)\)", data, re.DOTALL)]))

print("P1:", extract_sum(inp))
print("P2:", extract_sum("".join([s.split("don't()")[0] for s in inp.split("do()")])))