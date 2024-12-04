import sys, re
from functools import reduce

# string = 'blmul(44,46)umomul(123,4)fart'

# pattern = re.compile(r"mul\([0-9]+,[0-9]+\)")
# string_re = pattern.search(string).group()
# print(string_re)

pattern_in_rstr = r"mul\([0-9]+,[0-9]+\)"
# matches = re.findall(pattern_in_rstr, string)

# print(matches)


# mult_str = 'mul(22,14)'
pattern_mult_rstr = r'mul\(([0-9]+),([0-9]+)\)'
# pattern_groups = re.search(pattern_mult_rstr, mult_str)

# print(pattern_groups.groups())
# result = reduce(lambda x, y: int(x)*int(y), pattern_groups.groups())
# print(result)

with open(sys.argv[1], 'rt') as in_f:
    in_line = in_f.read().replace('\n', '')

matches = re.findall(pattern_in_rstr, in_line)
print(matches)

result = sum([
    reduce(
        lambda x, y: int(x) * int(y), 
        re.search(pattern_mult_rstr, match).groups()
    ) 
    for match in matches
])

print(result)

# correct: 183669043