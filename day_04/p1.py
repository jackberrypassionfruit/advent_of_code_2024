import sys

with open(sys.argv[1]) as in_f:
    hor_lines = in_f.read().split('\n')
input_width = len(hor_lines[0])
hor_str =  '_'.join(hor_lines)

vert_lines = [ ''.join([line[i] for line in hor_lines]) for i in range(input_width) ]
vert_str = '_'.join(vert_lines)


#  rotate all rows left by i, to make diagonal lines align as vertical
deg60_aligned_lines = [ ('_' * (input_width - ind)) + line + ('_' * ind) for ind, line in enumerate(hor_lines)]
deg60_aligned_vert_lines = [ '_' + ''.join([line[i] for line in deg60_aligned_lines]) + '_' for i in range(input_width*2) ]
deg60_aligned_vert_str = ''.join(deg60_aligned_vert_lines)


hor_lines_rev = [line[::-1] for line in hor_lines]
#  rotate all rows left by i, to make diagonal lines align as vertical
deg120_aligned_lines = [ ('_' * (input_width - ind)) + line + ('_' * ind) for ind, line in enumerate(hor_lines_rev)]
deg120_aligned_vert_lines = [ '_' + ''.join([line[i] for line in deg120_aligned_lines]) + '_' for i in range(input_width*2) ]
deg120_aligned_vert_str = ''.join(deg120_aligned_vert_lines)

total_str = hor_str + vert_str + deg60_aligned_vert_str + deg120_aligned_vert_str

# print(hor_str)
# print(vert_str)
# print(deg60_aligned_vert_str)
# print(deg120_aligned_vert_str)
# print(total_str)

print(total_str.count('XMAS') + total_str.count('SAMX'))

# correct: 2468