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
        self.path_coords_v = set()
        self.path_coords_h = set()
        self.turn_num = 0
        self.step_num = 0
        
        self.con = duckdb.connect()
        self.con.sql("CREATE TABLE ob_coords (x INTEGER, y INTEGER)")
        self.con.sql('''
        CREATE TABLE path_coords (
            x INTEGER, 
            y INTEGER,
            dir TEXT, 
            turn_num INTEGER
        );
            
        CREATE SEQUENCE id_sequence START 1;
        
        ALTER TABLE path_coords ADD COLUMN pk_id INTEGER DEFAULT nextval('id_sequence');
                     
        ''')

        for v, line in enumerate(lines):
            for h, char in enumerate(line):
                if char == '#':
                    self.con.sql(f"INSERT INTO ob_coords VALUES ({h}, {v})")
                    
                elif char == self.dir:
                    self.plr_coord = (h, v)
                    self.start_coord = self.plr_coord
                    self.plr_x = h
                    self.plr_y = v

    def __repr__(self) -> None:
        val = ''
        for v, line in enumerate(lines):
            for h, char in enumerate(line):
                if (h, v) == self.start_coord:
                    val += 'S'
                elif h == self.plr_x and v == self.plr_y:
                    val += self.dir
                elif (h, v) in self.path_coords_v and (h, v) in self.path_coords_h:
                    val += '+'
                elif (h, v) in self.path_coords_v:
                    val += '|'
                elif (h, v) in self.path_coords_h:
                    val += '-'
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
                WHERE x = {self.plr_x}  AND y < {self.plr_y} 
                ORDER BY y DESC LIMIT 1
            ''').fetchall()
            if new_y_result:
                new_y = new_y_result[0][0]
                self.path_coords_v.update(set([(self.plr_x, y) for y in range(new_y, self.plr_y + 1)]))
                self.con.sql(f'''
                    INSERT INTO path_coords (x, y, dir, turn_num)
                    SELECT 
                        {self.plr_x} AS x
                        ,i AS y
                        ,'{self.dir}' AS dir
                        ,{self.turn_num} AS turn_num
                    FROM generate_series({new_y}, {self.plr_y}) AS t(i)
                ''')
                self.plr_y = new_y
                self.dir = '>'
            else:
                self.path_coords_v.update(set([(self.plr_x, y) for y in range(0, self.plr_y + 1)]))
                self.con.sql(f'''
                    INSERT INTO path_coords (x, y, dir, turn_num)
                    SELECT 
                        i AS x
                        ,{self.plr_y} AS y
                        ,'{self.dir}' AS dir
                        ,{self.turn_num} AS turn_num
                    FROM generate_series(0, {self.plr_y}) AS t(i)
                ''')
                return 1
        elif self.dir == '>':
            new_x_result = self.con.sql(f'''
                SELECT x - 1 AS new_x FROM ob_coords 
                WHERE y = {self.plr_y} AND {self.plr_x} < x 
                ORDER BY x ASC LIMIT 1
            ''').fetchall()
            if new_x_result:
                new_x = new_x_result[0][0]
                self.path_coords_h.update(set([(x, self.plr_y) for x in range(self.plr_x, new_x + 1)]))
                self.con.sql(f'''
                    INSERT INTO path_coords (x, y, dir, turn_num)
                    SELECT 
                        i AS x
                        ,{self.plr_y} AS y
                        ,'{self.dir}' AS dir
                        ,{self.turn_num} AS turn_num
                    FROM generate_series({self.plr_x}, {new_x}) AS t(i)
                ''')
                self.plr_x = new_x
                self.dir = 'v'
            else:
                self.path_coords_h.update(set([(x, self.plr_y) for x in range(self.plr_x, len(lines[0]))]))
                self.con.sql(f'''
                    INSERT INTO path_coords (x, y, dir, turn_num)
                    SELECT 
                        {self.plr_x} AS x
                        ,i AS y
                        ,'{self.dir}' AS dir
                        ,{self.turn_num} AS turn_num
                    FROM generate_series({self.plr_x}, {len(lines[0]) - 1}) AS t(i)
                ''')
                return 1
        elif self.dir == 'v':
            new_y_result = self.con.sql(f'''
                SELECT y - 1 AS new_y FROM ob_coords 
                WHERE x = {self.plr_x} AND y > {self.plr_y} 
                ORDER BY y ASC LIMIT 1
            ''').fetchall()
            if new_y_result:
                new_y = new_y_result[0][0]
                self.path_coords_v.update(set([(self.plr_x, y) for y in range(self.plr_y, new_y + 1)]))
                self.con.sql(f'''
                    INSERT INTO path_coords (x, y, dir, turn_num)
                    SELECT 
                        {self.plr_x} AS x
                        ,i AS y
                        ,'{self.dir}' AS dir
                        ,{self.turn_num} AS turn_num
                    FROM generate_series({self.plr_y}, {new_y}) AS t(i)
                ''')
                self.plr_y = new_y
                self.dir = '<'
            else:
                self.path_coords_v.update(set([(self.plr_x, y) for y in range(self.plr_y, len(lines))]))
                self.con.sql(f'''
                    INSERT INTO path_coords (x, y, dir, turn_num)
                    SELECT 
                        {self.plr_x} AS x
                        ,i AS y
                        ,'{self.dir}' AS dir
                        ,{self.turn_num} AS turn_num
                    FROM generate_series({self.plr_y}, {len(lines) - 1}) AS t(i)
                ''')
                return 1
        elif self.dir == '<':
            new_x_result = self.con.sql(f'''
                SELECT x + 1 AS new_x FROM ob_coords 
                WHERE y = {self.plr_y} AND {self.plr_x} > x 
                ORDER BY x DESC LIMIT 1
            ''').fetchall()
            if new_x_result:
                new_x = new_x_result[0][0]
                self.path_coords_h.update(set([(x, self.plr_y) for x in range(new_x, self.plr_x + 1)]))
                self.con.sql(f'''
                    INSERT INTO path_coords (x, y, dir, turn_num)
                    SELECT 
                        {self.plr_x} AS x
                        ,i AS y
                        ,'{self.dir}' AS dir
                        ,{self.turn_num} AS turn_num
                    FROM generate_series({new_x}, {self.plr_x}) AS t(i)
                ''')
                self.plr_x = new_x
                self.dir = '^'
            else:
                self.path_coords_h.update(set([(x, self.plr_y) for x in range(0, self.plr_x + 1)]))
                self.con.sql(f'''
                    INSERT INTO path_coords (x, y, dir, turn_num)
                    SELECT 
                        {self.plr_x} AS x
                        ,i AS y
                        ,'{self.dir}' AS dir
                        ,{self.turn_num} AS turn_num
                    FROM generate_series(0, {self.plr_x}) AS t(i)
                ''')
                return 1
        self.turn_num += 1
            
    def test_path(self):
        cur_x, cur_y = 4, 6
        cur_turn = 4
        
        self.con.sql(f'''
            -- SELECT * FROM path_coords
            
            SELECT
                *
            FROM path_coords
            WHERE 1=1
            AND turn_num >=0 
            AND turn_num <=3
            -- AND turn_num < {cur_turn} AND x = {cur_x} AND y < {cur_y}
        ''').show()

moved = Mover()

while not moved.take_turn():
    ...
    print(f'{moved.step_num=}')
    # time.sleep(.1)
    # print(moved)

print(moved)
print(len(moved.path_coords_v.union(moved.path_coords_h)))
moved.test_path()
        