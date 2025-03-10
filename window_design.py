import time

import serial
import serial.tools.list_ports

from PyQt5.QtWidgets import QMainWindow
from window import Ui_MainWindow

Host_Address = '0f00'
Broadcast_Address = 'ffff'

TXD_HEAD = '41542b4d45534800'
TXD_END = '0d0a'

RXD_HEAD = 'f1dd'

CMD_Report_ID = '03'
CMD_Start_Group = '04'
CMD_Stop_Group = '05'


class My_MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(My_MainWindow, self).__init__()

        self.port = None
        self.host = None

        self.port_flag = 0

        self.setupUi(self)  # 创建窗体对象

        self.Cluster_Init()  # 集群初始化

    def Cluster_Init(self):
        self.Start_pushButton.clicked.connect(self.Cluster_Start)
        self.Refresh_pushButton.clicked.connect(self.Cluster_Refresh)
        self.Stop_pushButton.clicked.connect(self.Cluster_Stop)

        self.State_pushButton1.clicked.connect(self.Cluster_State1)
        self.State_pushButton2.clicked.connect(self.Cluster_State2)
        self.State_pushButton3.clicked.connect(self.Cluster_State3)
        self.State_pushButton4.clicked.connect(self.Cluster_State4)
        self.State_pushButton5.clicked.connect(self.Cluster_State5)
        self.State_pushButton6.clicked.connect(self.Cluster_State6)

        self.Start_pushButton.setEnabled(True)
        self.Refresh_pushButton.setEnabled(True)
        self.Stop_pushButton.setEnabled(False)
        self.State_pushButton1.setEnabled(False)
        self.State_pushButton2.setEnabled(False)
        self.State_pushButton3.setEnabled(False)
        self.State_pushButton4.setEnabled(False)
        self.State_pushButton5.setEnabled(False)
        self.State_pushButton6.setEnabled(False)

        self.Cluster_Refresh()

    def Cluster_Refresh(self):
        port_list = list(serial.tools.list_ports.comports())

        self.port_flag = 0
        for port in port_list:
            if port[1].find('USB') != -1:
                index_left = port[1].find('(')
                index_right = port[1].find(')')
                self.port = port[1][index_left + 1:index_right]
                self.port_flag = 1

    def Cluster_Start(self):
        self.Cluster_Refresh()

        if self.port_flag:
            self.host = serial.Serial(self.port, 9600, timeout=0.5)
            self.State_textBrowser.append('INFO: 串口 ' + self.port + ' 打开')

            self.Start_pushButton.setEnabled(False)
            self.Refresh_pushButton.setEnabled(False)
            self.Stop_pushButton.setEnabled(True)
            self.State_pushButton1.setEnabled(True)
            self.State_pushButton2.setEnabled(True)
            self.State_pushButton3.setEnabled(True)
            self.State_pushButton4.setEnabled(True)
            self.State_pushButton5.setEnabled(True)
            self.State_pushButton6.setEnabled(True)
        else:
            self.State_textBrowser.append('WARN: 未发现串口设备')

    def Cluster_Stop(self):
        if self.host.is_open:
            self.host.write(bytes.fromhex(TXD_HEAD + Broadcast_Address + CMD_Stop_Group + '01' + TXD_END))
            time.sleep(0.05)

            self.host.write(bytes.fromhex(TXD_HEAD + Broadcast_Address + CMD_Stop_Group + '02' + TXD_END))
            time.sleep(0.05)

            self.host.write(bytes.fromhex(TXD_HEAD + Broadcast_Address + CMD_Stop_Group + '03' + TXD_END))
            time.sleep(0.05)

            self.host.write(bytes.fromhex(TXD_HEAD + Broadcast_Address + CMD_Stop_Group + '04' + TXD_END))
            time.sleep(0.05)

            self.host.write(bytes.fromhex(TXD_HEAD + Broadcast_Address + CMD_Stop_Group + '05' + TXD_END))
            time.sleep(0.05)

            self.host.write(bytes.fromhex(TXD_HEAD + Broadcast_Address + CMD_Stop_Group + '06' + TXD_END))
            time.sleep(0.05)

            self.host.write(bytes.fromhex(TXD_HEAD + Broadcast_Address + CMD_Stop_Group + '07' + TXD_END))
            time.sleep(0.05)

            self.State_textBrowser.append('INFO: 所有机器人停止')

        else:
            self.State_textBrowser.append('ERROR: 串口断开')

    def Cluster_State1(self):
        if self.host.is_open:
            write_data = bytes.fromhex(TXD_HEAD + Broadcast_Address + '11' + '02' + '1032' + '000000000000' + TXD_END)
            self.host.write(write_data)
            time.sleep(0.05)

            write_data = bytes.fromhex(TXD_HEAD + Broadcast_Address + '11' + '03' + '0032' + '000000000000' + TXD_END)
            self.host.write(write_data)
            time.sleep(0.05)

            write_data = bytes.fromhex(TXD_HEAD + Broadcast_Address + '11' + '04' + '1032' + '000000000000' + TXD_END)
            self.host.write(write_data)
            time.sleep(0.05)

            write_data = bytes.fromhex(TXD_HEAD + Broadcast_Address + '11' + '05' + '0032' + '000000000000' + TXD_END)
            self.host.write(write_data)
            time.sleep(0.05)

            write_data = bytes.fromhex(TXD_HEAD + Broadcast_Address + '11' + '06' + '1032' + '000000000000' + TXD_END)
            self.host.write(write_data)
            time.sleep(0.05)

            write_data = bytes.fromhex(TXD_HEAD + Broadcast_Address + '11' + '07' + '0032' + '000000000000' + TXD_END)
            self.host.write(write_data)
            time.sleep(0.05)

            self.State_textBrowser.append('INFO: 控制指令1发送')
        else:
            self.State_textBrowser.append('ERROR: 串口断开')

    def Cluster_State2(self):
        if self.host.is_open:
            write_data = bytes.fromhex(TXD_HEAD + Broadcast_Address + '11' + '02' + '1096' + '000000000000' + TXD_END)
            self.host.write(write_data)
            time.sleep(0.05)

            write_data = bytes.fromhex(TXD_HEAD + Broadcast_Address + '11' + '03' + '0000' + '000000000000' + TXD_END)
            self.host.write(write_data)
            time.sleep(0.05)

            write_data = bytes.fromhex(TXD_HEAD + Broadcast_Address + '11' + '04' + '1096' + '000000000000' + TXD_END)
            self.host.write(write_data)
            time.sleep(0.05)

            write_data = bytes.fromhex(TXD_HEAD + Broadcast_Address + '11' + '05' + '0000' + '000000000000' + TXD_END)
            self.host.write(write_data)
            time.sleep(0.05)

            write_data = bytes.fromhex(TXD_HEAD + Broadcast_Address + '11' + '06' + '1096' + '000000000000' + TXD_END)
            self.host.write(write_data)
            time.sleep(0.05)

            write_data = bytes.fromhex(TXD_HEAD + Broadcast_Address + '11' + '07' + '0000' + '000000000000' + TXD_END)
            self.host.write(write_data)
            time.sleep(0.05)

            self.State_textBrowser.append('INFO: 控制指令2发送')
        else:
            self.State_textBrowser.append('ERROR: 串口断开')

    def Cluster_State3(self):
        if self.host.is_open:
            write_data = bytes.fromhex(TXD_HEAD + Broadcast_Address + '11' + '02' + '1096' + '000000000000' + TXD_END)
            self.host.write(write_data)
            time.sleep(0.05)

            write_data = bytes.fromhex(TXD_HEAD + Broadcast_Address + '11' + '03' + '1064' + '000000000000' + TXD_END)
            self.host.write(write_data)
            time.sleep(0.05)

            write_data = bytes.fromhex(TXD_HEAD + Broadcast_Address + '11' + '04' + '1096' + '000000000000' + TXD_END)
            self.host.write(write_data)
            time.sleep(0.05)

            write_data = bytes.fromhex(TXD_HEAD + Broadcast_Address + '11' + '05' + '1064' + '000000000000' + TXD_END)
            self.host.write(write_data)
            time.sleep(0.05)

            write_data = bytes.fromhex(TXD_HEAD + Broadcast_Address + '11' + '06' + '1096' + '000000000000' + TXD_END)
            self.host.write(write_data)
            time.sleep(0.05)

            write_data = bytes.fromhex(TXD_HEAD + Broadcast_Address + '11' + '07' + '1064' + '000000000000' + TXD_END)
            self.host.write(write_data)
            time.sleep(0.05)

            self.State_textBrowser.append('INFO: 控制指令3发送')
        else:
            self.State_textBrowser.append('ERROR: 串口断开')

    def Cluster_State4(self):
        if self.host.is_open:
            write_data = bytes.fromhex(TXD_HEAD + Broadcast_Address + '11' + '02' + '1064' + '000000000000' + TXD_END)
            self.host.write(write_data)
            time.sleep(0.05)

            write_data = bytes.fromhex(TXD_HEAD + Broadcast_Address + '11' + '03' + '1032' + '000000000000' + TXD_END)
            self.host.write(write_data)
            time.sleep(0.05)

            write_data = bytes.fromhex(TXD_HEAD + Broadcast_Address + '11' + '04' + '1064' + '000000000000' + TXD_END)
            self.host.write(write_data)
            time.sleep(0.05)

            write_data = bytes.fromhex(TXD_HEAD + Broadcast_Address + '11' + '05' + '1032' + '000000000000' + TXD_END)
            self.host.write(write_data)
            time.sleep(0.05)

            write_data = bytes.fromhex(TXD_HEAD + Broadcast_Address + '11' + '06' + '1064' + '000000000000' + TXD_END)
            self.host.write(write_data)
            time.sleep(0.05)

            write_data = bytes.fromhex(TXD_HEAD + Broadcast_Address + '11' + '07' + '1032' + '000000000000' + TXD_END)
            self.host.write(write_data)
            time.sleep(0.05)

            self.State_textBrowser.append('INFO: 控制指令4发送')
        else:
            self.State_textBrowser.append('ERROR: 串口断开')

    def Cluster_State5(self):
        if self.host.is_open:

            self.State_textBrowser.append('INFO: 控制指令5发送')
        else:
            self.State_textBrowser.append('ERROR: 串口断开')

    def Cluster_State6(self):
        if self.host.is_open:

            self.State_textBrowser.append('INFO: 控制指令6发送')
        else:
            self.State_textBrowser.append('ERROR: 串口断开')
