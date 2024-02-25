from mainUI import *
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Signal, QThread
import sys

console_buff = []
socket_list = []


# Socket线程类
class SocketThread(QThread):
    server_info_signal = Signal(str, int)
    data_received_signal = Signal(str)
    host = None
    port = None

    def __init__(self):
        super().__init__()
        self.server_info_signal[str, int].connect(self.get_server_inf)

    def run(self):
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            socket_list.append(s)
            socket_list[0].connect((self.host, self.port))
            socket_list[0].send("connect".encode('utf-8'))
            self.receive_data()
    
    def receive_data(self):
        while True:
            data = socket_list[0].recv(1024)
            self.data_received_signal.emit(data.decode("utf-8"))

    def get_server_inf(self, host: str, port: int):
        self.host = host
        self.port = port


class MainWindow(QMainWindow, Ui_MainWindow):
    command_submit_signal = Signal(str)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.socket_thread = None
        self.setupUi(self)
        self.command_submit_signal[str].connect(self.update_console)

    # 网络连接
    def connect_server(self):
        if self.label_state.text() == "未连接":
            self.update_console("正在尝试连接{}:{}".format(self.lineEdit_ip.text(), self.lineEdit_port.text()))
            self.socket_thread = SocketThread()
            self.socket_thread.start()
            self.socket_thread.server_info_signal.emit(self.lineEdit_ip.text(), int(self.lineEdit_port.text()))
            self.socket_thread.data_received_signal[str].connect(self.update_console)

    # 控制台函数
    def update_console(self, msg: str):
        import datetime
        console_buff.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "   " + msg)
        console_text = ""
        for line in console_buff:
            console_text += line + "\r"
        self.textEdit_console.setText(console_text)

    def command_submit(self):
        if self.lineEdit_command_line.text() != "":
            self.command_submit_signal.emit(self.lineEdit_command_line.text())
            self.lineEdit_command_line.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MyApp = MainWindow()
    MyApp.show()
    sys.exit(app.exec())