import regex as re
import sys

pattern_x_max = r'MAS|SAM'

with open(sys.argv[1]) as in_f:
    hor_lines = in_f.read().split('\n')
input_width = len(hor_lines[0])

vert_lines = [ ''.join([line[i] for line in hor_lines]) for i in range(input_width) ]


deg60_coords = set()
#  rotate all rows left by i, to make diagonal lines align as vertical
deg60_aligned_lines = [ ('_' * (input_width - ind)) + line + ('_' * ind) for ind, line in enumerate(hor_lines)]
deg60_aligned_vert_lines = [ ''.join([line[i] for line in deg60_aligned_lines]) for i in range(1, input_width*2) ]
# deg60_aligned_vert_str = ''.join(deg60_aligned_vert_lines)
# for line in deg60_aligned_lines:
#     print(line)
for index, line in enumerate(deg60_aligned_vert_lines):
    # print(line)
    new_coords = [(match.start() - (input_width - index - 2), match.start() + 1) for match in re.finditer(pattern_x_max, line, overlapped=True) ]
    # print(new_coords)
    deg60_coords.update(new_coords)

# print(sorted(list(deg60_coords), key=lambda t: t[0]))

deg120_coords = set()
hor_lines_rev = [line[::-1] for line in hor_lines]
#  rotate all rows left by i, to make diagonal lines align as vertical
deg120_aligned_lines = [ ('_' * (input_width - ind)) + line + ('_' * ind) for ind, line in enumerate(hor_lines_rev)]
deg120_aligned_vert_lines = [ '_' + ''.join([line[i] for line in deg120_aligned_lines]) + '_' for i in range(input_width*2) ]
# deg120_aligned_vert_str = ''.join(deg120_aligned_vert_lines)
# for line in deg120_aligned_lines:
#     print(line)
for index, line in enumerate(deg120_aligned_vert_lines):
    # print(line)
    new_coords = [(input_width - (match.start() - (input_width - index - 1)), match.start()) for match in re.finditer(pattern_x_max, line, overlapped=True) ]
    # print(new_coords)
    deg120_coords.update(new_coords)

# print(sorted(list(deg120_coords), key=lambda t: t[0]))

coords = deg60_coords.intersection(deg120_coords)

print(sorted(list(coords), key=lambda t: t[0]))
print(len(coords))