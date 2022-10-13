import sqlite3
import os

def save_db(db):
    db.conn.commit()

def close_db(db):
    db.conn.commit()
    db.conn.close()

class EasyDB:
    def __init__(self, db_file):
        self.file = db_file
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
    def execute(self, *query):
        return self.cursor.execute(*query)
    def delete(self):
        os.remove(self.file)
    def create_table(self, table_name, *column_names):
        query_1 = "(" + ", ".join(column_names) + ")"
        self.cursor.execute(f"CREATE TABLE {table_name} {query_1}")

class DBTable:
    def __init__(self, db, table):
        self.db = db
        self.table = table
    def __repr__(self):
        return f"Table {self.table} in database {self.db.file}"
    def get_column(self, column):
        return [item[0] for item in self.db.cursor.execute(f"SELECT {column} FROM {self.table}")]
    def insert_values(self, **values):
        column_names = [description[0] for description in self.db.execute(f"SELECT * FROM {self.table}").description]
        query_1 = "(" + ", ".join(column_names) + ")"
        query_2 = "(" + ", ".join(["?" for _ in range(len(column_names))]) + ")"
        query_3 = (values.get(column_names[0], None), values.get(column_names[1], None))
        self.db.cursor.execute(f'''INSERT INTO {self.table} {query_1} VALUES {query_2}''', query_3)
        self.db.cursor.commit()

class DBKey:
    def __init__(self, db_table, key, value):
        self.db = db_table.db
        self.key = key
        self.value = value
        self.table = db_table.table
    def __getitem__(self, key):
        print(self.key)
        print(key)
        output = [item for item in self.db.cursor.execute(f'''
        SELECT
            {self.value}
        FROM
            {self.table}
        WHERE
            {self.key} = ?
        ''', key)][0]
        if len(output) == 1:
            output = output[0]
        return output
    def exists(self, key):
        output = [item for item in self.db.cursor.execute(f'SELECT * FROM {self.table} WHERE {self.key} = username')]
        print(output)
        for x in output:
            if(x[0] == key):
                return True
        return False
    def __setitem__(self, key, newvalue):
        self.db.cursor.execute(f'''
        UPDATE
            {self.table}
        SET
            {self.value} = ?
        WHERE
            {self.key} = ?
        ''', (newvalue, key))