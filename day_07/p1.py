import sys
from math import log, ceil, floor
from functools import reduce


class Bish:
    def __init__(self):
        with open(sys.argv[1]) as in_f:
            lines = in_f.read().split('\n')
    
        self.calibrations = {
            line.split(': ')[0]: line.split(': ')[1].split(' ')
            for line
            in lines
        }    
        self.bin_op_index = 0

# for key, val in calibrations.items():
#     # print(f'{key=}, {val=}')
#     ...
#     num_ops = len(val)-1
    

# num_ops = 8
# for n in range(1, num_ops+1):
#     num_places = ceil(log(num_ops, 2))
#     bin_str = ('0' * num_places) + bin(n)[2:]
#     print(bin_str[-num_places:], end=':  ')
#     print(''.join(['+' if num == '1' else '-' for num in bin_str[-num_places:]]))

# bin_ops_list = [ list((('0' * ceil(log(num_ops, 2))) + bin(n)[2:])[-ceil(log(num_ops, 2)):]) for n in range(1, num_ops+1) ]

# for op in bin_ops_list:
#     print(op)

# key='292'
# vals=['11', '6', '16', '20']
# bin_ops = ['1', '0', '1']
# bin_op_index = 0 # global

    def calc_op_combos(self, key, vals):
        num_ops = 2**(len(vals)-1)
        bin_ops_list = [ 
            list((('0' * ceil(log(num_ops, 2))) + bin(n)[2:])[-ceil(log(num_ops, 2)):]) 
            for n 
            in range(num_ops)
        ]
        # print(bin_ops_list)
        for bin_ops in bin_ops_list:
            self.bin_op_index = 0
            def bin_op_and_index(a, b):
                a, b = int(a), int(b)
                if bin_ops[self.bin_op_index] == '1':
                    out = a * b
                else:
                    out = a + b
                self.bin_op_index += 1
                return out
            
            res = reduce(bin_op_and_index, vals)
            # print(f'{bin_ops=} --- {vals} --- {res}')
            if int(key) == res:
                return res
        return 0
            
    def check_input(self):
        sum_yes = 0
        for key, calib in self.calibrations.items():
            sum_yes += self.calc_op_combos(key, calib)  
                          
        return sum_yes
        
bish = Bish()
res = bish.calc_op_combos(key=292, vals=['11', '6', '16', '20'])
    
# print(f'{res=}')
print(bish.check_input())
# 210 too low