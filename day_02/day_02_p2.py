import sys

with open(sys.argv[1], 'rt') as in_f:
    lines = in_f.read().split('\n')

def test_list(list_nums):
    sorted_test =   all([ 1  <= list_nums[i] - list_nums[i+1] <= 3  for i in range(len(list_nums) - 1)]) or \
                    all([ -3 <= list_nums[i] - list_nums[i+1] <= -1 for i in range(len(list_nums) - 1)])
    return sorted_test

def test_list_w_skips(list_nums):
    sorted_test =   all([ 1  <= list_nums[i] - list_nums[i+1] <= 3  or 1  <= list_nums[i] - list_nums[i+2] <= 3  for i in range(len(list_nums) - 2)]) or \
                    all([ -3 <= list_nums[i] - list_nums[i+1] <= -1 or -3 <= list_nums[i] - list_nums[i+2] <= -1 for i in range(len(list_nums) - 2)])
    # sorted_test =   sorted_test and (
    #     all([ list_nums[i] < list_nums[i+1] for i in range(len(list_nums) - 2)]) or \
    #     all([ list_nums[i] > list_nums[i+1] for i in range(len(list_nums) - 2)])
    # )
    return sorted_test

def all_list_once_removed(list_nums):
    test_lists = [ list_nums[:i] + list_nums[i+1:] for i in range(0, len(list_nums)) ]
    return [list_nums] + test_lists

# test_nums = [int(char) for char in '3 6 5 4'.split()]
# for test_list in all_list_once_removed(test_nums):
#     print(test_list)


# tested_list = ['Safe' if any(test_list(this_list) for this_list in all_list_once_removed([int(char) for char in line.split()])) else 'Unsafe' for line in lines]
# tested_list = ['Safe' if test_list([int(char) for char in line.split()]) else 'Unsafe' for line in lines]
# for nums, test in zip(lines, tested_list):
#     print(f'{nums} - {test}')

tested_sum = sum([any(test_list(this_list) for this_list in all_list_once_removed([int(char) for char in line.split()])) for line in lines])
print(f'{tested_sum=}')

# too high: 720

# correct: 689

# too low: 682
# too low: 670