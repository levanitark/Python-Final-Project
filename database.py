import sqlite3

class Database:
    def __init__(self, db_path="./dist/data.sqlite3"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def get_columns(self, table):
        query = f"SELECT * FROM {table} LIMIT 1"
        self.cursor.execute(query)
        column_names = [col[0] for col in self.cursor.description]
        return column_names

    def insert(self, table, full_values):
        placeholders = ','.join(['?'] * len(full_values))
        query = f"INSERT INTO {table} VALUES ({placeholders})"
        self.cursor.execute(query, full_values)
        self.conn.commit()

    def update(self, table, columns, values, row_id):
        set_clause = ', '.join([f"{col}=?" for col in columns[1:]])
        query = f"UPDATE {table} SET {set_clause} WHERE {columns[0]}=?"
        self.cursor.execute(query, values[1:] + [row_id])
        self.conn.commit()

    def delete(self, table, col_id, row_id):
        query = f"DELETE FROM {table} WHERE {col_id}=?"
        self.cursor.execute(query, (row_id,))
        self.conn.commit()
