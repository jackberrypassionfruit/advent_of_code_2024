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
        self.turn_num = 0
        self.step_num = 0
        
        self.con = duckdb.connect('my_database.db')
        self.con.sql("CREATE OR REPLACE TABLE ob_coords (x INTEGER, y INTEGER)")
        self.con.sql('''
        CREATE OR REPLACE TABLE path_coords (
            x INTEGER, 
            y INTEGER,
            dir TEXT, 
            turn_num INTEGER
        );
        
        DROP SEQUENCE id_sequence;
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
                elif (h, v) in self.con.sql("SELECT x, y FROM path_coords WHERE dir IN ('^', 'v')").fetchall() and \
                    (h, v) in self.con.sql("SELECT x, y FROM path_coords WHERE dir IN ('<', '>')").fetchall():
                    val += '+'
                elif (h, v) in self.con.sql("SELECT x, y FROM path_coords WHERE dir IN ('^', 'v')").fetchall():
                    val += '|'
                elif (h, v) in self.con.sql("SELECT x, y FROM path_coords WHERE dir IN ('<', '>')").fetchall():
                    val += '-'
                elif char == '#':
                    val += '#'
                else:
                    val += '.'
            val += '\n'
        with open('repr_file.txt', 'w') as out_f:
            out_f.write(val)
        return ''
        # return val

    def take_turn(self):
        if self.dir == '^':
            select = 'MAX(y) + 1 AS new_y'
            where = f'x = {self.plr_x}  AND y < {self.plr_y}'
            order = 'y'
            next_dir = '>'
            x, y = self.plr_x, 'i'
        elif self.dir == '>':
            select = 'MIN(x) - 1 AS new_x'
            where = f'y = {self.plr_y} AND {self.plr_x} < x'
            order = 'x'
            next_dir = 'v'
            x, y = 'i', self.plr_y
        elif self.dir == 'v':
            select = 'MIN(y) - 1 AS new_y'
            where = f'x = {self.plr_x} AND y > {self.plr_y}'
            order = 'y'
            next_dir = '<'
            x, y = self.plr_x, 'i'
        elif self.dir == '<':
            select = 'MAX(x) + 1 AS new_x'
            where = f'y = {self.plr_y} AND {self.plr_x} > x'
            order = 'x'
            next_dir = '^'
            x, y = 'i', self.plr_y
            
        new_result = self.con.sql(f'''
            SELECT {select} FROM ob_coords 
            WHERE {where}
            GROUP BY {order}
            -- ORDER BY {order} DESC LIMIT 1
        ''').fetchall()
        
        if new_result:
            new_val = new_result[0][0]
            
            if self.dir == '^':
                turn_series = f'{new_val}, {self.plr_y}'
                self.plr_y = new_val
            elif self.dir == '>':
                turn_series = f'{self.plr_x}, {new_val}'
                self.plr_x = new_val
            elif self.dir == 'v':
                turn_series = f'{self.plr_y}, {new_val}'
                self.plr_y = new_val
            elif self.dir == '<':
                turn_series = f'{new_val}, {self.plr_x}'
                self.plr_x = new_val
                
            self.con.sql(f'''
                INSERT INTO path_coords (x, y, dir, turn_num)
                SELECT 
                    {x} AS x
                    ,{y} AS y
                    ,'{self.dir}' AS dir
                    ,{self.turn_num} AS turn_num
                FROM generate_series({turn_series}) AS t(i)
            ''')
                
            self.dir = next_dir
            
        else:
            if self.dir == '^':
                end_series = f'0, {self.plr_y}'
            elif self.dir == '>':
                end_series = f'{self.plr_x}, {len(lines[0]) - 1}'
            elif self.dir == 'v':
                end_series = f'{self.plr_y}, {len(lines) - 1}'
            elif self.dir == '<':
                end_series = f'0, {self.plr_x}'
            self.con.sql(f'''
                INSERT INTO path_coords (x, y, dir, turn_num)
                SELECT 
                    {x} AS x
                    ,{y} AS y
                    ,'{self.dir}' AS dir
                    ,{self.turn_num} AS turn_num
                FROM generate_series({end_series}) AS t(i)
            ''')
            return 1   
        
        self.turn_num += 1
            
    def get_path_blockers_num(self):
        path_blockers = self.con.sql(f'''
SELECT
	COUNT(*)
FROM (
	SELECT DISTINCT
		a.*
	FROM main.path_coords AS a
	INNER JOIN main.path_coords AS b
	ON 
		a.turn_num > b.turn_num
		AND CASE
			WHEN a.dir = '^'
				THEN b.dir = '>'
				AND a.y = b.y
				AND a.x < b.x
			WHEN a.dir = 'v'
				THEN b.dir = '<'
				AND a.y = b.y
				AND a.x > b.x
			WHEN a.dir = '>'
				THEN b.dir = 'v'
				AND a.x = b.x
				AND a.y < b.y
			WHEN a.dir = '<'
				THEN b.dir = '^'
				AND a.x = b.x
				AND a.y > b.y
		END
) AS x
        ''').fetchall()[0][0]
        
        return path_blockers

moved = Mover()

while not moved.take_turn():
    ...
    # time.sleep(.1)
    # print(moved)

print(moved)
print(moved.get_path_blockers_num())
# definitely not 4