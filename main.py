import sys

from ui.ui_lab8 import Ui_MainWindow
from ui.ui_create import Ui_Dialog
from core.db_connection import Column, Table, Connection

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


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
            return 1

        return len(self.table.garbage)
    
    def columnCount(self, *args, **kwargs):
        if not self.table:
            return 1

        return len(self.table.columns)

    def setTable(self, table: Table):
        self.beginResetModel()
        self.table = table
        self.endResetModel()

    def getIndex(self, index: QModelIndex, role: Qt.ItemDataRole):
        if not index.isValid() or not self.table or not self.table.garbage:
            return
        
        if role == Qt.ItemDataRole.DisplayRole:
            return self.table.garbage[index.row()][0]

    def data(self, index: QModelIndex, role: Qt.ItemDataRole):
        if not index.isValid() or not self.table or not self.table.garbage:
            return

        if role == Qt.ItemDataRole.DisplayRole:
            return self.table.garbage[index.row()][index.column()]

    def headerData(self, section, orientation, role):
        if not (role == Qt.ItemDataRole.DisplayRole and
            orientation == Qt.Orientation.Horizontal and
            self.table):
            return

        return {
            i:self.table.columns[i].name for i in range(self.columnCount())
        }.get(section)




class Window(QMainWindow):
    def __init_conn(self):
        self.conn = Connection()
        self.conn.create_connection(db_port=5430, db_user='admin', db_passwd='admin',
                           db_name='lab8')
        self.conn.drop_all()
        self.conn.fill_default()
        self.conn.fill_data()


    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.model = ItemsModel()
        self.ui.tablesListView.setModel(self.model)
        self.ui.tablesListView.clicked.connect(self.select_from_table)

        self.__init_conn()
        self.tables = self.conn.load_tables()
        self.listTables = Table(table_name='', garbage=[
            [i, self.tables[i].table_name] for i in range(len(self.tables))
        ], columns_names=['num', 'name'])
        self.model.setTable(self.listTables)

        self.ui.addButton.clicked.connect(self.ui_open_create_window)
        self.ui.editButton.clicked.connect(self.ui_open_edit_window)
        self.ui.deleteButton.clicked.connect(self.ui_open_delete_window)


    def ui_open_create_window(self):
        self.create_window = Ui_Dialog()
        self.ui.setupUi(self.create_window)
        self.create_window.show()
        sender = self.sender()
        if sender.text() == "Add":
            self.ui.addButton.clicked.connect(self.add_new_item())


    def ui_open_edit_window(self):
        index = self.ui.tableInfoView.selectedIndexes()[0]
        id = str(self.ui.tableInfoView.model().data(index))


    def ui_open_delete_window(self):
        index = self.ui.tableInfoView.selectedIndexes()[0]
        id = str(self.ui.tableInfoView.model().data(index))

    def select_from_table(self):
        role = Qt.ItemDataRole.DisplayRole
        index = self.ui.tablesListView.selectedIndexes()[0]
        id = str(self.ui.tablesListView.model().getIndex(index, role))

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
