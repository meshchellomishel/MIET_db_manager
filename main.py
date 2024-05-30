import sys

from ui.ui_lab8 import Ui_MainWindow
from ui import ui_create
from ui import ui_delete
from ui import ui_edit
from core.db_connection import Column, Table, Connection

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog


def test():
    conn = Connection()
    conn.create_connection(db_port=5430, db_user='admin', db_passwd='admin',
                           db_name='lab8')
    conn.drop_all()
    conn.fill_default()
    conn.fill_data()

    args = Table(table_name='Заявки', args={
        'id': "'21'",
        'Name': "'Иванов Иван Иванович'",
        'Phone': "'1234567890'",
        'Receipt': "'1'",
        'Bank': "'Сбербанк'",
        'Account': "'12345678901234567890'",
        'Address': "'ул. Ленина, 1'",
        'District': "'Центральный'",
        'DateStart': "'2024-03-01'",
        'Document': "'Паспорт'",
        'Speed': "'1'",
        'DateStop': 'NULL',
        'Cost': "'10000'",
    })
    conn.add_new_transaction_query(args)

    args = Table(table_name='Выдача', args={
        'id': "'21'",
        'Finish': "'0'",
    })
    conn.add_new_transaction_query(args)

    tables = conn.load_tables()
    [print(i.pretty()) for i in tables]

    conn.close_connection()


class ItemsModel(QAbstractTableModel):
    def __init__(self, *args, **kwargs) -> None:
        self.table = None
        super().__init__(*args, **kwargs)
    
    def setItems(self, items):
        pass

    def setRegion(self, regions):
        pass

    def rowCount(self, *args, **kwargs):
        if not self.table:
            return 0

        return len(self.table.garbage)
    
    def columnCount(self, *args, **kwargs):
        if not self.table:
            return 0

        return len(self.table.columns)

    def setTable(self, table: Table):
        self.beginResetModel()
        self.table = table
        self.endResetModel()

    def getColumnNameIndex(self, index: QModelIndex, role: Qt.ItemDataRole):
        if not index.isValid() or not self.table or not self.table.garbage:
            return
        
        if role == Qt.ItemDataRole.DisplayRole:
            return self.table.columns[index.column()].name

    def getIndex(self, index: QModelIndex, role: Qt.ItemDataRole):
        if not index.isValid() or not self.table or not self.table.garbage:
            return
        
        if role == Qt.ItemDataRole.DisplayRole:
            return self.table.garbage[index.row()][0]

    def data(self, index: QModelIndex, role: Qt.ItemDataRole):
        if not index.isValid() or not self.table or not self.table.garbage:
            return

        if role == Qt.ItemDataRole.DisplayRole:
            return str(self.table.garbage[index.row()][index.column()])

    def headerData(self, section, orientation, role):
        if not (role == Qt.ItemDataRole.DisplayRole and
            orientation == Qt.Orientation.Horizontal and
            self.table):
            return

        return {
            i:self.table.columns[i].name for i in range(self.columnCount())
        }.get(section)


class Dialog(QDialog):
    pass


class Window(QMainWindow):
    def __init_conn(self):
        self.conn = Connection()
        self.conn.create_connection(db_port=5430, db_user='admin', db_passwd='admin',
                           db_name='lab8')
        self.conn.drop_all()
        self.conn.fill_default()
        self.conn.fill_data()

    def __update_tables(self):
        self.tables = self.conn.load_tables()
        self.listTables = Table(table_name='', garbage=[
            [i, self.tables[i].table_name] for i in range(len(self.tables))
        ], columns_names=['num', 'name'])
        self.model.setTable(self.listTables)

    def __update_info_table(self, id):
        table = self.tables[id]
        data = self.conn.select_transaction_query(table)
        table.setGarbage(garbage=data)
        self.infoModel.setTable(table)

    def __get_lastInfoTable(self):
        return self.tables[self.lastTableId]

    def __get_lastInfoNameTable(self):
        return self.__get_lastInfoTable().table_name

    def __init__(self):
        super(Window, self).__init__()
        self.lastTableId = 0
        self.create_dialog = Dialog()
        self.delete_dialog = Dialog()
        self.update_dialog = Dialog()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.model = ItemsModel()
        self.infoModel = ItemsModel()
        self.ui.tablesListView.setModel(self.model)
        self.ui.tableInfoView.setModel(self.infoModel)
        self.ui.tablesListView.clicked.connect(self.select_from_table)

        self.__init_conn()
        self.__update_tables()

        self.ui.addButton.clicked.connect(self.ui_open_create_window)
        self.ui.editButton.clicked.connect(self.ui_open_edit_window)
        self.ui.deleteButton.clicked.connect(self.ui_open_delete_window)

    def __get_info_tables_index(self):
        role = Qt.ItemDataRole.DisplayRole
        index = self.ui.tableInfoView.selectedIndexes()
        if not index:
            return

        index = index[0]
        id = int(self.ui.tableInfoView.model().getIndex(index, role))
        return id


    def create_item(self):
        columns = self.__get_lastInfoTable().columns_names
        args = {}
        for i in range(len(columns)):
            if self.create_data[i] != None:
                args[columns[i]] = f"'{self.create_data[i]}'"

        table = Table(
            table_name=self.__get_lastInfoNameTable(),
            args=args
        )
        self.lastQuery = self.conn.query_build_insert(table)
        self.conn.add_new_transaction_query(table)

    def on_create_accepted(self):
        create_data = self.create_window.textCreate.toPlainText()
        create_data = create_data.replace(' ', '')
        create_data = create_data.split(';')
        self.create_data = create_data
        try:
            self.create_item()
        except Exception as e:
            self.ui.status_label.setText('Failed to execute ' + self.lastQuery)
            self.create_dialog.close()
            raise e

        self.__update_info_table(self.lastTableId)
        self.create_dialog.close()

    def ui_open_create_window(self):
        if not self.lastTableId:
            return

        self.create_window = ui_create.Ui_Dialog()
        self.create_window.setupUi(self.create_dialog)
        self.create_dialog.show()

        self.create_window.buttonBox.accepted.connect(self.on_create_accepted)
        self.create_window.buttonBox.rejected.connect(self.create_dialog.close)


    def edit_item(self):
        self.conn.update_transaction_query(Table(
            table_name=self.__get_lastInfoNameTable(),
            args={
                'id': self.edit_id,
                self.edit_column: self.edit_data
            }
        ))

    def on_edit_accepted(self):
        self.edit_data = self.edit_window.editField.toPlainText()
        try:
            self.edit_item()
        except Exception as e:
            self.update_dialog.close()
            raise e

        if not self.lastTableId:
            return
        
        self.__update_info_table(self.lastTableId)
        self.update_dialog.close()

    def ui_open_edit_window(self):
        role = Qt.ItemDataRole.DisplayRole
        index = self.ui.tableInfoView.selectedIndexes()
        if not index:
            return

        index = index[0]
        id = int(self.ui.tableInfoView.model().getIndex(index, role))
        column_name = self.ui.tableInfoView.model().getColumnNameIndex(index, role)
        if not id or not column_name:
            return

        self.edit_window = ui_edit.Ui_Dialog()
        self.edit_window.setupUi(self.update_dialog)
        self.update_dialog.show()

        self.edit_id = id
        self.edit_column = column_name
        self.edit_window.buttonBox.accepted.connect(self.on_edit_accepted)
        self.edit_window.buttonBox.rejected.connect(self.update_dialog.close)

    def delete_tiem(self):
        self.conn.delete_transaction_query(Table(
            table_name=self.__get_lastInfoNameTable(),
            args={
                'id': self.delete_id
            }
        ))

    def on_delete_accepted(self):
        try:
            self.delete_tiem()
        except Exception as e:
            self.delete_dialog.close()
            raise e

        if not self.lastTableId:
            return
        
        self.__update_info_table(self.lastTableId)
        self.delete_dialog.close()

    def ui_open_delete_window(self):
        id = self.__get_info_tables_index()
        if not id:
            return

        self.delete_window = ui_delete.Ui_Dialog()
        self.delete_window.setupUi(self.delete_dialog)
        self.delete_dialog.show()

        self.delete_id = id
        self.delete_window.buttonBox.accepted.connect(self.on_delete_accepted)
        self.delete_window.buttonBox.rejected.connect(self.delete_dialog.close)

    def select_from_table(self):
        role = Qt.ItemDataRole.DisplayRole
        index = self.ui.tablesListView.selectedIndexes()
        if not index:
            return

        index = index[0]
        id = int(self.ui.tablesListView.model().getIndex(index, role))
        self.lastTableId = id
        self.__update_info_table(id)

    def delete_new_item(self):
        pass


    def edit_new_item(self):
        pass


    def add_new_item(self):
        pass


    def create_element(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()

    sys.exit(app.exec())
