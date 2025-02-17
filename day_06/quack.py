
import duckdb

with duckdb.connect('my_database.db') as con:
    con.sql(f'''
    SELECT
        *
        ,ROW_NUMBER() OVER () AS row_num
    FROM path_coords
''').show()

