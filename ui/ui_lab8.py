# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'lab8.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialogButtonBox, QHBoxLayout,
    QHeaderView, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QTableView, QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        font = QFont()
        font.setFamilies([u"Ubuntu Light"])
        MainWindow.setFont(font)
        MainWindow.setToolTipDuration(1)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(350, 10, 91, 31))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(30, 60, 181, 31))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(280, 60, 91, 31))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(340, 430, 91, 31))
        self.buttonBox = QDialogButtonBox(self.centralwidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(620, 550, 166, 24))
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.queryEdit = QTextEdit(self.centralwidget)
        self.queryEdit.setObjectName(u"queryEdit")
        self.queryEdit.setGeometry(QRect(20, 479, 731, 51))
        self.tableInfoView = QTableView(self.centralwidget)
        self.tableInfoView.setObjectName(u"tableInfoView")
        self.tableInfoView.setGeometry(QRect(280, 90, 471, 331))
        self.tablesListView = QTableView(self.centralwidget)
        self.tablesListView.setObjectName(u"tablesListView")
        self.tablesListView.setGeometry(QRect(20, 90, 201, 331))
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(500, 60, 254, 25))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.editButton = QPushButton(self.layoutWidget)
        self.editButton.setObjectName(u"editButton")

        self.horizontalLayout_3.addWidget(self.editButton)

        self.addButton = QPushButton(self.layoutWidget)
        self.addButton.setObjectName(u"addButton")

        self.horizontalLayout_3.addWidget(self.addButton)

        self.deleteButton = QPushButton(self.layoutWidget)
        self.deleteButton.setObjectName(u"deleteButton")

        self.horizontalLayout_3.addWidget(self.deleteButton)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Lab8", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Lab8", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Tables", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Table info", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Query", None))
        self.editButton.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.addButton.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.deleteButton.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
    # retranslateUi

