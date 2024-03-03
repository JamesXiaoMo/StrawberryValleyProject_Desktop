import os
import time

from mainUI import *
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Signal, QThread
import sys
import plotly.offline as pyof
import plotly.graph_objs as go
import pandas as pd

console_buff = []
socket_dictionary = {}


# Socket线程类
class SocketThread(QThread):
    server_info_signal = Signal(str, int)
    data_received_signal = Signal(str)

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
            s.send("connect".encode('utf-8'))
            self.receive_data()

    def receive_data(self):
        while True:
            data = socket_dictionary["main"].recv(1024)
            self.data_received_signal.emit(data.decode("utf-8"))

    def get_server_inf(self, host: str, port: int):
        self.host = host
        self.port = port


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
            os.chdir(os.getcwd() + os.sep + "graphs")
            time.sleep(1)
            socket_dictionary["file_download"].send(self.parameter.encode('utf-8'))
            with open(self.parameter + "_data.json", "wb") as f:
                while True:
                    data = socket_dictionary["file_download"].recv(1024)
                    if data.decode('utf-8') == "end":
                        break
                    f.write(data)
            print('Download complete')
            time.sleep(1)
            socket_dictionary["file_download"].close()

    def get_server_inf(self, host: str, port: int):
        self.host = host
        self.port = port


class MainWindow(QMainWindow, Ui_MainWindow):
    command_submit_signal = Signal(str)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.file_download_thread = None
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

    # 图表函数
    def get_graph(self, json_name: str):
        graph_path = os.getcwd()
        os.chdir(graph_path)
        data_graph = pd.read_json(graph_path + os.sep + json_name)
        # data_graph = pd.read_excel("data_table.xlsx")
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
        pyof.plot(fig, filename=graph_path + os.sep + "graph.html", auto_open=False)
        self.webEngineView.setUrl(QUrl.fromLocalFile(graph_path + os.sep + "graph.html"))

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MyApp = MainWindow()
    MyApp.show()
    sys.exit(app.exec())
