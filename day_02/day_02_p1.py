import sys

with open(sys.argv[1], 'rt') as in_f:
    lines = in_f.readlines()

def test_list(list_nums):
    sorted_test =   all([ 1  <= list_nums[i] - list_nums[i+1] <= 3  for i in range(len(list_nums) - 1)]) or \
                    all([ -3 <= list_nums[i] - list_nums[i+1] <= -1 for i in range(len(list_nums) - 1)])
    return sorted_test

tested_list = ['Safe' if test_list([int(char) for char in line.split()]) else 'Unsafe' for line in lines]
# for test in tested_list:
#     print(test)

tested_sum = sum([test_list([int(char) for char in line.split()]) for line in lines])
print(f'{tested_sum=}')