import sys, time
import pandas as pd
import polars as pl
import duckdb

with open(sys.argv[1]) as in_f:
    lines = in_f.read().split('\n')
    
    
class Mover():
    def __init__(self):
        self.dir = '^'
        self.plr_x, self.plr_y = 0, 0
        self.path_coords = set()
        
        self.ob_coords = []
        self.ob_coords_df = pl.DataFrame()
        self.con = duckdb.connect()
        self.con.sql("CREATE TABLE ob_coords (x INTEGER, y INTEGER)")

        for v, line in enumerate(lines):
            for h, char in enumerate(line):
                if char == '#':
                    self.ob_coords.append((h, v))
                    self.ob_coords_df = pl.concat(
                        [
                            self.ob_coords_df,
                            pl.DataFrame({
                                'x': h,
                                'y': v
                            })
                        ]
                    )
                    self.con.sql(f"INSERT INTO ob_coords VALUES ({h}, {v})")
                    
                elif char == self.dir:
                    self.plr_coord = (h, v)
                    self.plr_x = h
                    self.plr_y = v

    def __repr__(self) -> None:
        val = ''
        for v, line in enumerate(lines):
            for h, char in enumerate(line):
                if h == self.plr_x and v == self.plr_y:
                    val += self.dir
                elif (h, v) in self.path_coords:
                    val += 'X'
                elif char == '#':
                    val += '#'
                else:
                    val += '.'
            val += '\n'
        return val

    def take_turn(self):   
        if self.dir == '^':
            new_y_result = self.con.sql(f'''
                SELECT y + 1 AS new_y FROM ob_coords 
                WHERE x = {self.plr_x} 
                AND y < {self.plr_y} 
                ORDER BY y DESC 
                LIMIT 1
            ''').fetchall()
            if new_y_result:
                new_y = new_y_result[0][0]
                self.path_coords.update(set([(self.plr_x, y) for y in range(new_y, self.plr_y + 1)]))
                self.plr_y = new_y
                self.dir = '>'
            else:
                self.path_coords.update(set([(self.plr_x, y) for y in range(0, self.plr_y + 1)]))
                return 1
        elif self.dir == '>':
            new_x_result = self.con.sql(f'''
                SELECT x - 1 AS new_x FROM ob_coords 
                WHERE y = {self.plr_y} 
                AND {self.plr_x} < x 
                ORDER BY x ASC 
                LIMIT 1
            ''').fetchall()
            if new_x_result:
                new_x = new_x_result[0][0]
                self.path_coords.update(set([(x, self.plr_y) for x in range(self.plr_x, new_x + 1)]))
                self.plr_x = new_x
                self.dir = 'v'
            else:
                self.path_coords.update(set([(x, self.plr_y) for x in range(self.plr_x, len(lines[0]))]))
                return 1
        elif self.dir == 'v':
            new_y_result = self.con.sql(f'''
                SELECT y - 1 AS new_y FROM ob_coords 
                WHERE x = {self.plr_x} 
                AND y > {self.plr_y} 
                ORDER BY y ASC 
                LIMIT 1
            ''').fetchall()
            if new_y_result:
                new_y = new_y_result[0][0]
                self.path_coords.update(set([(self.plr_x, y) for y in range(self.plr_y, new_y + 1)]))
                self.plr_y = new_y
                self.dir = '<'
            else:
                self.path_coords.update(set([(self.plr_x, y) for y in range(self.plr_y, len(lines))]))
                return 1
        elif self.dir == '<':
            new_x_result = self.con.sql(f'''
                SELECT x + 1 AS new_x FROM ob_coords 
                WHERE y = {self.plr_y} 
                AND {self.plr_x} > x 
                ORDER BY x DESC 
                LIMIT 1
            ''').fetchall()
            if new_x_result:
                new_x = new_x_result[0][0]
                self.path_coords.update(set([(x, self.plr_y) for x in range(new_x, self.plr_x + 1)]))
                self.plr_x = new_x
                self.dir = '^'
            else:
                self.path_coords.update(set([(x, self.plr_y) for x in range(0, self.plr_x + 1)]))
                return 1

moved = Mover()
# print(moved)

while not moved.take_turn():
    ...
    # time.sleep(.1)
    # print(moved)

print(moved)
print(len(moved.path_coords))
        