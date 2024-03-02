# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
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
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QTabWidget, QTextEdit,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(700, 400)
        MainWindow.setMinimumSize(QSize(700, 400))
        MainWindow.setMaximumSize(QSize(700, 400))
        icon = QIcon()
        icon.addFile(u"pics/main.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        self.centralwidget.setMinimumSize(QSize(700, 400))
        self.centralwidget.setMaximumSize(QSize(700, 400))
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QRect(0, 0, 700, 400))
        self.tab_1 = QWidget()
        self.tab_1.setObjectName(u"tab_1")
        self.textEdit_console = QTextEdit(self.tab_1)
        self.textEdit_console.setObjectName(u"textEdit_console")
        self.textEdit_console.setGeometry(QRect(0, 0, 550, 350))
        self.textEdit_console.setReadOnly(True)
        self.lineEdit_command_line = QLineEdit(self.tab_1)
        self.lineEdit_command_line.setObjectName(u"lineEdit_command_line")
        self.lineEdit_command_line.setGeometry(QRect(0, 350, 470, 22))
        self.pushButton_command_submit = QPushButton(self.tab_1)
        self.pushButton_command_submit.setObjectName(u"pushButton_command_submit")
        self.pushButton_command_submit.setGeometry(QRect(470, 350, 80, 22))
        self.label = QLabel(self.tab_1)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(560, 0, 120, 30))
        font = QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_2 = QLabel(self.tab_1)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(560, 30, 53, 15))
        font1 = QFont()
        font1.setPointSize(10)
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.lineEdit_ip = QLineEdit(self.tab_1)
        self.lineEdit_ip.setObjectName(u"lineEdit_ip")
        self.lineEdit_ip.setGeometry(QRect(560, 50, 120, 20))
        self.label_3 = QLabel(self.tab_1)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(560, 80, 53, 15))
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.lineEdit_port = QLineEdit(self.tab_1)
        self.lineEdit_port.setObjectName(u"lineEdit_port")
        self.lineEdit_port.setGeometry(QRect(560, 100, 120, 20))
        self.pushButton_connect = QPushButton(self.tab_1)
        self.pushButton_connect.setObjectName(u"pushButton_connect")
        self.pushButton_connect.setGeometry(QRect(560, 150, 120, 22))
        self.label_state = QLabel(self.tab_1)
        self.label_state.setObjectName(u"label_state")
        self.label_state.setGeometry(QRect(560, 130, 60, 15))
        self.label_state.setFont(font1)
        self.label_state.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_delay = QLabel(self.tab_1)
        self.label_delay.setObjectName(u"label_delay")
        self.label_delay.setGeometry(QRect(625, 130, 53, 15))
        self.label_delay.setFont(font1)
        self.label_delay.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.webEngineView = QWebEngineView(self.tab_2)
        self.webEngineView.setObjectName(u"webEngineView")
        self.webEngineView.setGeometry(QRect(0, 0, 694, 372))
        self.webEngineView.setUrl(QUrl(u"about:blank"))
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        MainWindow.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.tabWidget, self.textEdit_console)
        QWidget.setTabOrder(self.textEdit_console, self.lineEdit_ip)
        QWidget.setTabOrder(self.lineEdit_ip, self.lineEdit_port)
        QWidget.setTabOrder(self.lineEdit_port, self.pushButton_connect)
        QWidget.setTabOrder(self.pushButton_connect, self.lineEdit_command_line)
        QWidget.setTabOrder(self.lineEdit_command_line, self.pushButton_command_submit)

        self.retranslateUi(MainWindow)
        self.pushButton_command_submit.clicked.connect(MainWindow.command_submit)
        self.pushButton_connect.clicked.connect(MainWindow.connect_server)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"StrawberryValley Alpha-0.0.1", None))
        self.lineEdit_command_line.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u6307\u4ee4", None))
        self.pushButton_command_submit.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u670d\u52a1\u5668\u8bbe\u7f6e", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"IP\u5730\u5740", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u7aef\u53e3", None))
        self.pushButton_connect.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5", None))
        self.label_state.setText(QCoreApplication.translate("MainWindow", u"\u672a\u8fde\u63a5", None))
        self.label_delay.setText(QCoreApplication.translate("MainWindow", u"0 ms", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), QCoreApplication.translate("MainWindow", u"\u63a7\u5236\u53f0", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u56fe\u8868", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
    # retranslateUi

