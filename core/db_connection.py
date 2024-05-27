import psycopg2
from .default import tables, values


class Table:
    def _getColumns(self, args):
        columns = []
        for arg in args.keys():
            columns.append(arg)
        return columns

    def __init__(self, table_name: str, args: dict):
        self.table_name = table_name
        self.args = args
        self.columns = self._getColumns(args)

    def setArgs(self, args):
        self.args = args
        self.columns = self._getColumns(args)
    
    def setTable_name(self, table_name):
        self.table_name = table_name

    def formatUpdateArgs(self):
        buf = []
        res = []

        for i in self.columns:
            if i != 'id':
                buf.append(i)
        
        for i in buf:
            res.append(f"{i}={self.args[i]}")
        
        return ",".join(res)

    def formatValues(self):
        return ','.join(list(self.args.values()))

    def formatColumns(self):
        return ','.join(list(self.args.keys()))

    def formatArgs(self):
        return list(self.args.values())


class Connection:
    def _assert_window(self, f):
        if not f:
            return False
        return True


    def create_connection(self, db_name='postgres', db_port=5432, db_addr='127.0.0.1',
                          db_user='postgres', db_passwd='postgres'):
        self.conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_passwd,
                                     host=db_addr, port=db_port)
        self.cursor = self.conn.cursor()

    
    def execute_query_with_params(self, sql_query):
        self._assert_window(not self.conn.closed)
        print(f"[INFO]: executing: {sql_query}")
        self.cursor.execute(sql_query)
    
    def add_new_transaction_query(self, table: Table):
        sql_query = f"INSERT INTO {table.table_name} ({table.formatColumns()}) VALUES ({table.formatValues()})"
        self.execute_query_with_params(sql_query)

    def update_transaction_query(self, table: Table):
        sql_query = f"UPDATE {table.table_name} SET {table.formatUpdateArgs()} WHERE ID={table.args['id']}"
        self.execute_query_with_params(sql_query)

    def delete_transaction_query(self, table: Table):
        sql_query = f"DELETE FROM {table.table_name} WHERE ID={table.args['id']}"
        self.execute_query_with_params(sql_query)
    
    def drop_all(self):
        self.cursor.execute(
            '''
                DROP TABLE IF EXISTS Заявки CASCADE;
                DROP TABLE IF EXISTS Выдача CASCADE;
                DROP TABLE IF EXISTS Выход_техника CASCADE;
                DROP TABLE IF EXISTS Исполнение CASCADE;
                DROP TABLE IF EXISTS Оплата CASCADE;
            '''
        )
    
    def fill_data(self):
        self.cursor.execute(
            values
        )

    def fill_default(self):
        self.cursor.execute(
            tables
        )

    def close_connection(self):
        self.cursor.close()
        self.conn.close()