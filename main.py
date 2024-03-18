import os
import time

import ping3
import schedule

from mainUI import *
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Signal, QThread
import sys
import plotly.offline as pyof
import plotly.graph_objs as go
import pandas as pd

console_buff = []
socket_dictionary = {}
socket_busy = False
main_path = os.getcwd()
socket_status = True


# 客户端向服务器发送String的函数
def s_send(msg: str) -> None:
    global socket_busy
    if socket_dictionary["main"] is not None:
        while socket_busy:
            time.sleep(1)
            pass
        socket_busy = True
        socket_dictionary["main"].send(msg.encode('utf-8'))
        socket_busy = False


# 定时任务线程类
class ScheduledTasksThread(QThread):
    server_info_signal = Signal(str, int)
    delay_signal = Signal(int)

    def __init__(self):
        super().__init__()
        self.host = None
        self.port = None
        self.server_info_signal[str, int].connect(self.get_server_inf)
        schedule.every(1).minute.do(self.delay_test)

    def run(self):
        self.delay_test()
        import schedule
        import time
        while True:
            schedule.run_pending()
            time.sleep(1)

    def delay_test(self) -> None:
        if self.host is not None:
            delay = ping3.ping(self.host) * 1000
            self.delay_signal.emit(int(round(delay)))

    def get_server_inf(self, host: str, port: int) -> None:
        self.host = host
        self.port = port


# Socket连接线程类
class SocketThread(QThread):
    server_info_signal = Signal(str, int)
    console_signal = Signal(str)
    login_signal = Signal(str)
    pushbutton_connect_signal = Signal(int)
    label_state_signal = Signal(int)

    def __init__(self):
        super().__init__()
        self.port = None
        self.host = None
        self.server_info_signal[str, int].connect(self.get_server_inf)

    def run(self):
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            socket_dictionary["main"] = s
            s.connect((self.host, self.port))
            time.sleep(1)
            s.send("CONNECT_FD".encode("utf-8"))
            self.receive_data()

    def receive_data(self):
        datalist = [0]
        try:
            while True:
                data = socket_dictionary["main"].recv(1024).decode('utf-8')
                print(data)
                if data == "CONNECT_FD_OK":
                    self.console_signal.emit("服务器连接成功")
                    self.pushbutton_connect_signal.emit(1)
                    self.label_state_signal.emit(1)
                elif data == "CONNECT_FD_ERROR":
                    self.console_signal.emit("服务器连接失败")
                elif data == "LOGIN_OK":
                    self.console_signal.emit("登录成功")
                elif data == "LOGIN_ERROR":
                    self.console_signal.emit("登录失败")
                elif data == "DELAY_REPLY":
                    pass
                if "-" in data:
                    datalist = data.split('-')
        except ConnectionAbortedError:
            self.console_signal.emit("客户端断开连接")

    def get_server_inf(self, host: str, port: int):
        self.host = host
        self.port = port


# 文件下载线程类
class FileDownloadThread(QThread):
    server_info_signal = Signal(str, int)
    graph_update_signal = Signal(str)

    def __init__(self, parameter: str):
        super().__init__()
        self.parameter = parameter
        self.port = None
        self.host = None
        self.server_info_signal[str, int].connect(self.get_server_inf)

    def run(self):
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            socket_dictionary["file_download"] = s
            s.connect((self.host, self.port))
            self.receive_data()
            self.graph_update_signal.emit(self.parameter + "_data.json")

    def receive_data(self):
        if socket_dictionary["file_download"] is not None:
            os.chdir(main_path + os.sep + "graphs")
            socket_dictionary["file_download"].send(self.parameter.encode('utf-8'))
            with open(self.parameter + "_data.json", "wb") as f:
                while True:
                    data = socket_dictionary["file_download"].recv(1024)
                    if data.decode('utf-8') == "end":
                        break
                    f.write(data)
            print('Download complete')
            os.chdir(main_path)
            socket_dictionary["file_download"].close()
            socket_dictionary["file_download"] = None

    def get_server_inf(self, host: str, port: int):
        self.host = host
        self.port = port


class MainWindow(QMainWindow, Ui_MainWindow):
    command_submit_signal = Signal(str)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.scheduled_tasks_thread = None
        self.file_download_thread = None
        self.socket_thread = None
        self.setupUi(self)
        self.command_submit_signal[str].connect(self.update_console)
        self.dateEdit.setDate(QDate.currentDate())
        self.lineEdit_pwd.setEchoMode(QLineEdit.EchoMode.Password)

    # 网络连接
    def connect_server(self):
        global socket_status
        if self.pushButton_connect.text() == "连接":
            socket_status = True
            self.update_console("正在尝试连接{}:{}".format(self.lineEdit_ip.text(), self.lineEdit_port.text()))
            self.socket_thread = SocketThread()
            self.scheduled_tasks_thread = ScheduledTasksThread()
            self.socket_thread.start()
            self.socket_thread.pushbutton_connect_signal[int].connect(self.update_pushbutton_connect)
            self.scheduled_tasks_thread.start()
            self.socket_thread.server_info_signal.emit(self.lineEdit_ip.text(), int(self.lineEdit_port.text()))
            self.scheduled_tasks_thread.server_info_signal.emit(self.lineEdit_ip.text(), int(self.lineEdit_port.text()))
            self.socket_thread.console_signal[str].connect(self.update_console)
            self.scheduled_tasks_thread.delay_signal[int].connect(self.update_delay)
            self.socket_thread.label_state_signal[int].connect(self.update_label_state)
        elif self.pushButton_connect.text() == "断开连接":
            socket_dictionary["main"].close()
            socket_dictionary["main"] = None
            self.socket_thread.pushbutton_connect_signal.emit(0)
            self.socket_thread.label_state_signal.emit(0)
            socket_status = False

    # 控制台函数
    def update_console(self, msg: str):
        import datetime
        console_buff.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "   " + msg)
        console_text = ""
        for line in console_buff:
            console_text += line + "\r"
        self.textEdit_console.setText(console_text)

    def update_delay(self, delay: int) -> None:
        self.label_delay.setText("{} ms".format(str(delay)))
        if delay < 20:
            self.label_delay.setStyleSheet("color: green;")
        elif 20 <= delay <= 80:
            self.label_delay.setStyleSheet("color: orange;")
        elif delay > 80:
            self.label_delay.setStyleSheet("color: red;")

    def update_pushbutton_connect(self, status: int) -> None:
        if status == 0:
            self.pushButton_connect.setText("连接")
        elif status == 1:
            self.pushButton_connect.setText("断开连接")

    def update_label_state(self, status: int) -> None:
        if status == 0:
            self.label_state.setText("未连接")
            self.label_state.setStyleSheet("color: red;")
        elif status == 1:
            self.label_state.setText("已连接")
            self.label_state.setStyleSheet("color:green")

    def command_submit(self):
        if self.lineEdit_command_line.text() != "":
            self.command_submit_signal.emit(self.lineEdit_command_line.text())
            self.lineEdit_command_line.clear()

    # 图表函数
    def get_graph(self, json_name: str):
        os.chdir(main_path + os.sep + "graphs" + os.sep)
        data_graph = pd.read_json(json_name)
        hum = go.Scatter(
            x=data_graph["current_time"],
            y=data_graph["data_air_hum"],
            name="湿度",
            connectgaps=True
        )
        temp = go.Scatter(
            x=data_graph["current_time"],
            y=data_graph["data_air_temp"],
            name="温度",
            connectgaps=True
        )
        data = [hum, temp]
        layout = dict(
            title="温湿度图表",
            xaxis=dict(title="日期"),
            yaxis=dict(title="温度/湿度"))
        fig = go.Figure(data=data, layout=layout)
        pyof.plot(fig, filename="graph.html", auto_open=False)
        self.webEngineView.setUrl(QUrl.fromLocalFile(main_path + os.sep + "graphs" + os.sep + "graph.html"))
        os.chdir(main_path)
        print(os.getcwd())

    def get_hour_data(self):
        self.file_download_thread = FileDownloadThread("hour")
        self.file_download_thread.start()
        self.file_download_thread.server_info_signal.emit(self.lineEdit_ip.text(), int(self.lineEdit_port.text()))
        self.file_download_thread.graph_update_signal[str].connect(self.get_graph)

    def get_day_data(self):
        self.file_download_thread = FileDownloadThread("day")
        self.file_download_thread.start()
        self.file_download_thread.server_info_signal.emit(self.lineEdit_ip.text(), int(self.lineEdit_port.text()))
        self.file_download_thread.graph_update_signal[str].connect(self.get_graph)

    def get_week_data(self):
        self.file_download_thread = FileDownloadThread("week")
        self.file_download_thread.start()
        self.file_download_thread.server_info_signal.emit(self.lineEdit_ip.text(), int(self.lineEdit_port.text()))
        self.file_download_thread.graph_update_signal[str].connect(self.get_graph)

    def get_month_data(self):
        self.file_download_thread = FileDownloadThread("month")
        self.file_download_thread.start()
        self.file_download_thread.server_info_signal.emit(self.lineEdit_ip.text(), int(self.lineEdit_port.text()))
        self.file_download_thread.graph_update_signal[str].connect(self.get_graph)

    def get_year_data(self):
        self.file_download_thread = FileDownloadThread("year")
        self.file_download_thread.start()
        self.file_download_thread.server_info_signal.emit(self.lineEdit_ip.text(), int(self.lineEdit_port.text()))
        self.file_download_thread.graph_update_signal[str].connect(self.get_graph)

    def get_custom_data(self):
        pass

    # 用户登录函数
    def login(self):
        s_send("LOGIN_{USER_NAME}_{PASSWORD}".format(USER_NAME=self.lineEdit_username.text(),
                                                     PASSWORD=self.lineEdit_pwd.text()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MyApp = MainWindow()
    MyApp.show()
    sys.exit(app.exec())
