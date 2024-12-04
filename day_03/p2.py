import sys, re
from functools import reduce

with open(sys.argv[1], 'rt') as in_f:
    in_line = in_f.read().replace('\n', '')

def calc_mult_sums(in_str):
    pattern_in_rstr     = r"mul\([0-9]+,[0-9]+\)"
    pattern_mult_rstr   = r'mul\(([0-9]+),([0-9]+)\)'

    matches = re.findall(pattern_in_rstr, in_str)
    result = sum([
        reduce(
            lambda x, y: int(x) * int(y), 
            re.search(pattern_mult_rstr, match).groups()
        ) 
        for match in matches
    ])
    return result

# result = calc_mult_sums(in_line)
# print(result)

pattern_dont_rstr = r'don\'t\(\)'
found_dont_inds = [('dont', match.start()) for match in re.finditer(pattern_dont_rstr, in_line)]

pattern_do_rstr = r'do\(\)'
found_do_inds =   [('do', match.start()) for match in re.finditer(pattern_do_rstr,   in_line)]

# print(f'{found_dont_inds=}')
# print(f'{found_do_inds=}')

found_inds = found_dont_inds + found_do_inds
found_inds.sort(key=lambda ind: ind[1])
# print(f'{found_inds=}\n')

found_inds_filtered = [ found_inds[0]] + [ found_inds[i+1] for i in range(0, len(found_inds) - 1) if found_inds[i][0] != found_inds[i+1][0] ]
# first is "do", so I don't actually care about it # found_inds_filtered = [ found_inds[0]] + [ found_inds[i+1] for i in range(0, len(found_inds) - 1) if found_inds[i][0] != found_inds[i+1][0] ]
# print(f'{found_inds_filtered=}\n')

# found_inds_slices = [f"[{i}:{i+1}]" for i in range(0, len(found_inds_filtered) -1, 2)]
found_inds_slices = [f'[:{found_inds_filtered[1][1]}]'] + [f"[{found_inds_filtered[i][1]}:{found_inds_filtered[i+1][1]}]" for i in range(2, len(found_inds_filtered) - 1, 2)]
# print(f'{found_inds_slices=}\n')

in_line_filtered_list = [in_line[:found_inds_filtered[1][1]]] + [
    in_line[found_inds_filtered[i][1]:found_inds_filtered[i+1][1]]
    for i in range(2, len(found_inds_filtered) - 1, 2)
]

in_line_filtered = ''.join(in_line_filtered_list)
# print(f'{in_line_filtered=}')

result = calc_mult_sums(in_line_filtered)
print(result)

# correct baby!: 59097164