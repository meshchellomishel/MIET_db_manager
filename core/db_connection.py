import psycopg2
from .default import tables, values


class Value:
    def __init__(self, id, value) -> None:
        self.id = id
        self.value = value


class Column:
    def __init__(self, name, type=None) -> None:
        self.name = name
        self.type = type


class Table:
    def _getColumns(self, args):
        columns = []
        for arg in args.keys():
            columns.append(Column(name=arg))
        return columns

    def __init__(self, table_name: str, columns_names: list=None, columns: list=None,
                 values=None, args: dict={}, garbage=None):
        if columns_names:
            columns = [Column(name=i) for i in columns_names]

        if columns and len(columns) and not len(args):
            args = {i: None for i in columns}
            self.columns = columns
        else:
            self.columns = self._getColumns(args)

        self.columns_names = [i.name for i in self.columns]
        self.table_name = table_name
        self.args = args
        self.types = []
        self.values = values if values else []
        self.garbage = garbage if garbage else None

    def setGarbage(self, garbage):
        self.garbage = garbage

    def setArgs(self, args):
        self.args = args
        self.columns = self._getColumns(args)
    
    def setTable_name(self, table_name):
        self.table_name = table_name

    def setData(self, values):
        self.values = values

    def formatUpdateArgs(self):
        buf = []
        res = []

        for i in self.columns:
            if i.name != 'id':
                buf.append(i.name)
        
        for i in buf:
            res.append(f"{i}='{self.args[i]}'")
        
        return ",".join(res)

    def formatValues(self):
        return ','.join(list(self.args.values()))

    def formatColumns(self):
        return ','.join([i.name for i in self.columns])

    def formatArgs(self):
        return list(self.args.values())

    @staticmethod
    def list2Columns(columns: list):
        return [Column(name=i[0], type=i[1]) for i in columns]

    @staticmethod
    def list2Values(values):
        assert values
        assert len(values) != 0

        res = []
        for i in range(len(values)):
            res.append(Value(id=values[i][0], value=values[i][1::]))
        
        return res

    def pretty(self):
        return f'''
        [{self.table_name}]
        \t{" ".join([f"{i.name}:{i.type}" for i in self.columns])}
        \t{" ".join([f"{i.id}:{i.value}" for i in self.values])}
        '''


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
        try:
            return self.cursor.fetchall()
        except:
            pass
    
    
    def query_build_insert(self, table: Table):
        return f"INSERT INTO {table.table_name} ({table.formatColumns()}) VALUES ({table.formatValues()});"

    def query_build_update(self, table: Table):
        return f"UPDATE {table.table_name} SET {table.formatUpdateArgs()} WHERE ID={table.args['id']};"

    def query_build_delete(self, table: Table):
        return f"DELETE FROM {table.table_name} WHERE ID={table.args['id']};"

    def query_build_select(self, table: Table):
        return f"SELECT {table.formatColumns()} FROM {table.table_name} ORDER BY id"

    def add_new_transaction_query(self, table: Table):
        sql_query = self.query_build_insert(table)
        return self.execute_query_with_params(sql_query)

    def update_transaction_query(self, table: Table):
        sql_query = self.query_build_update(table)
        return self.execute_query_with_params(sql_query)

    def delete_transaction_query(self, table: Table):
        sql_query = self.query_build_delete(table)
        return self.execute_query_with_params(sql_query)
    
    def select_transaction_query(self, table: Table):
        sql_query = self.query_build_select(table)
        return self.execute_query_with_params(sql_query)

    def load_columns(self, table: Table):
        sql_query = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name='{table.table_name}';"
        return self.execute_query_with_params(sql_query)

    def load_tables(self):
        tables_columns, tables_data = [], []
        sql_query = f"SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname='public';"
        tables = self.execute_query_with_params(sql_query)
        tables = [i[0] for i in tables]
        for i in tables:
            cols = self.load_columns(Table(table_name=i))
            cols = Table.list2Columns(cols)
            tables_columns.append(cols)

            values = self.select_transaction_query(Table(table_name=i, columns=cols))
            values = Table.list2Values(values=values)
            tables_data.append(values)


        t_tables = [Table(table_name=tables[i], columns=tables_columns[i], values=tables_data[i])
                    for i in range(len(tables))]
        return t_tables


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