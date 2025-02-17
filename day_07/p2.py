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
        
    def alter_number_system_from_decimal(self, dec_num, to_num_sys):
        num_ops = to_num_sys**ceil(log(dec_num + 1, to_num_sys))
        num_places = int(log(num_ops, to_num_sys))
        new_sys_list = [ str(floor((dec_num % (to_num_sys**(n))) / (to_num_sys**(n-1)))) for n in range(num_places, 0, -1) ]
        new_sys_str = ''.join(new_sys_list)
        return new_sys_str

    def calc_op_combos(self, key, vals):
        num_ops = 3**(len(vals)-1)
        bin_ops_list = [ 
            list((('0' * ceil(log(num_ops, 3))) + self.alter_number_system_from_decimal(n, 3))[-ceil(log(num_ops, 3)):]) 
            for n 
            in range(num_ops)
        ]
        # print(bin_ops_list)
        for bin_ops in bin_ops_list:
            self.bin_op_index = 0
            def bin_op_and_index(a, b):
                a, b = int(a), int(b)
                if bin_ops[self.bin_op_index] == '0':
                    out = a * b
                elif bin_ops[self.bin_op_index] == '1':
                    out = a + b
                else:
                    out = int(str(a)+str(b))
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
# res = bish.calc_op_combos(key=156, vals=['15', '6'])
# print(f'{res=}')
    
print(bish.check_input())
# 148410216797310 too low


# dec_num = 9
# num_ops = 3**ceil(log(dec_num + 1, 3))

# # num_ops = 28
# print(f'{num_ops=}')


# num_places = int(log(num_ops, 3))
# print(f'{num_places=}')
# tern = ''.join([ str(floor((dec_num % (3**(n))) / (3**(n-1)))) for n in range(num_places, 0, -1) ])
# print(tern)

# for i in range(50):
#     to_num = bish.alter_number_system_from_decimal(i, 8)
#     print(f'{i}: {to_num}')
