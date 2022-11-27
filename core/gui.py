# -*- coding: UTF-8 -*- 
# Creator：LeK
# Date：2022/11/25


import threading
import asyncio
import sys
from PyQt5 import QtCore, uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDialog
from core import utils, bilidynamic, danmaku
import configparser
from PyQt5.Qt import QObject
from PyQt5.QtCore import pyqtSignal
import os
import ctypes

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")  # 任务栏图标


class MySignal(QObject):
    """
    自定义信号
    """
    textbroswer_print = pyqtSignal(str)


class cookie_widget(QDialog):
    """
    cookie窗口
    """
    config = configparser.RawConfigParser()
    bilicfgpath = utils.get_path('bili')

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(os.path.join(os.path.dirname(__file__), "GUI/cookie.ui"))  # 动态加载UI文件
        self.ui.setMaximumSize(QtCore.QSize(452,232))
        self.ui.setMinimumSize(QtCore.QSize(452,232))
        self.ui.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "GUI/img/windowicon.ico")))
        background_path = os.path.join(os.path.dirname(__file__), "GUI/img/cookie.jpg")
        self.ui.frame.setStyleSheet(
            '''
            QLabel{
                font-family:Georgia;
            }
            #frame{
            border-image:url(%s);
            }''' % background_path.replace('\\', '/'))
        cookie_widget.config.read(cookie_widget.bilicfgpath, encoding='utf-8')
        sessdata = cookie_widget.config['Cookie']['sessdata']
        bili_jct = cookie_widget.config['Cookie']['bili_jct']
        buvid3 = cookie_widget.config['Cookie']['buvid3']
        self.ui.sessdata_lineEdit.setText(sessdata)
        self.ui.bili_jct_lineEdit.setText(bili_jct)
        self.ui.buvid3_lineEdit.setText(buvid3)
        self.ui.buttonBox.clicked.connect(self.input_cookie)

    def input_cookie(self):
        sessdata = self.ui.sessdata_lineEdit.text()
        bili_jct = self.ui.bili_jct_lineEdit.text()
        buvid3 = self.ui.buvid3_lineEdit.text()
        cookie_widget.config.read(cookie_widget.bilicfgpath, encoding='utf-8')
        cookie_widget.config.remove_option('Cookie', 'sessdata')
        cookie_widget.config.remove_option('Cookie', 'prebili_jct')
        cookie_widget.config.remove_option('Cookie', 'buvid3')
        cookie_widget.config.set('Cookie', 'sessdata', sessdata)
        cookie_widget.config.set('Cookie', 'bili_jct', bili_jct)
        cookie_widget.config.set('Cookie', 'buvid3', buvid3)
        cookie_widget.config.write(open(cookie_widget.bilicfgpath, 'w'))
        reboot()


class MainWindow:
    """
    主窗口
    """
    config = configparser.RawConfigParser()
    bilicfgpath = utils.get_path('bili')
    loop = asyncio.new_event_loop()  # 创建事件循环传入模块
    asyncio.set_event_loop(loop)

    def __init__(self):
        # 初始化
        self.ui = uic.loadUi(os.path.join(os.path.dirname(__file__), "GUI/AsStudio.ui"))
        self.ui.setMaximumSize(QtCore.QSize(1099, 718))
        self.ui.setMinimumSize(QtCore.QSize(1099, 718))
        self.ui.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "GUI/img/windowicon.ico")))
        background_path = os.path.join(os.path.dirname(__file__), "GUI/img/background.jpg")
        self.ui.mainwindow.setStyleSheet(
            '''
            #mainwindow{
            border-image:url(%s);
            }''' % background_path.replace('\\', '/'))
        self.unable_button(self.ui.dynamiccloseButton)
        self.unable_button(self.ui.weathercloseButton)
        self.unable_button(self.ui.puzzlecloseButton)
        self.unable_button(self.ui.runcloseButton)
        self.filepath = utils.get_path("function")
        self.preroomid = None
        self.threads = []
        self.prestatus = {}
        self.danmaku_signal = MySignal()
        self.gift_signal = MySignal()
        self.danmaku_signal.textbroswer_print.connect(self.danmaku_printtext)
        self.gift_signal.textbroswer_print.connect(self.gift_printtext)
        self.init()
        self.danmaku = threading.Thread(target=danmaku.run, name='danmaku',
                                        args=(MainWindow.loop, self.danmaku_signal, self.gift_signal))  # 弹幕、礼物、入场记录线程
        self.bilidynamic = threading.Thread(target=bilidynamic.run, name='bilidynamic',
                                            args=(MainWindow.loop,))  # b站开播动态线程
        self.threads.append(self.danmaku)
        self.threads.append(self.bilidynamic)
        for thread in self.threads:
            thread.start()

        # 连接槽函数
        self.ui.dynamicokButton.clicked.connect(lambda: self.click_button(self.ui.dynamicokButton,
                                                                          self.ui.dynamiccloseButton, "dynamic", True))
        self.ui.dynamiccloseButton.clicked.connect(lambda: self.click_button(self.ui.dynamiccloseButton,
                                                                             self.ui.dynamicokButton, "dynamic", False))
        self.ui.weatherokButton.clicked.connect(lambda: self.click_button(self.ui.weatherokButton,
                                                                          self.ui.weathercloseButton, "getweather",
                                                                          True))
        self.ui.weathercloseButton.clicked.connect(lambda: self.click_button(self.ui.weathercloseButton,
                                                                             self.ui.weatherokButton, "getweather",
                                                                             False))
        self.ui.puzzleokButton.clicked.connect(lambda: self.click_button(self.ui.puzzleokButton,
                                                                         self.ui.puzzlecloseButton, "puzzle", True))
        self.ui.puzzlecloseButton.clicked.connect(lambda: self.click_button(self.ui.puzzlecloseButton,
                                                                            self.ui.puzzleokButton, "puzzle", False))
        self.ui.runokButton.clicked.connect(lambda: self.click_button(self.ui.runokButton,
                                                                      self.ui.runcloseButton, "connect", True))
        self.ui.runcloseButton.clicked.connect(lambda: self.click_button(self.ui.runcloseButton,
                                                                         self.ui.runokButton, "connect", False))
        self.ui.roomid.returnPressed.connect(self.get_roomid)
        self.ui.cookiebutton.clicked.connect(self.cookie_window)

    def unable_button(self, button):
        button.setEnabled(False)
        button.setStyleSheet(
            '''
            *{
                font-family:三极行楷简体-粗;
                color:rgba(148, 148, 148, 150);
                background-color:rgba(148, 148, 148, 150);
            }''')

    def enable_button(self, button):
        button.setEnabled(True)
        button.setStyleSheet(
            '''
            *{
                font-family:三极行楷简体-粗;
                color:rgb(255, 255, 255);
                background-color:rgba(255, 255, 255, 150);
            }''')

    def click_button(self, close_button, open_button, functionname: str, flag: bool):
        self.unable_button(close_button)
        self.enable_button(open_button)
        data = utils.read_json(self.filepath)
        data[functionname] = flag
        utils.write_json(data, self.filepath)
        if close_button is self.ui.runokButton:
            self.ui.roomid.setEnabled(False)
            self.ui.cookiebutton.setEnabled(False)
        elif close_button is self.ui.runcloseButton:
            self.ui.roomid.setEnabled(True)
            self.ui.cookiebutton.setEnabled(True)

    def get_roomid(self):
        room_id = self.ui.roomid.text()
        MainWindow.config.read(MainWindow.bilicfgpath, encoding='utf-8')
        MainWindow.config.remove_option('RoomsStatus', self.preroomid)
        MainWindow.config.set('RoomsStatus', room_id, '0')  # 写入直播间状态
        MainWindow.config.write(open(MainWindow.bilicfgpath, 'w'))
        reboot()

    def init(self):
        data = utils.read_json(self.filepath)
        data["dynamic"] = False
        data["puzzle"] = False
        data["getweather"] = False
        data["connect"] = False
        utils.write_json(data, self.filepath)
        MainWindow.config.read(MainWindow.bilicfgpath, encoding='utf-8')
        roomid = MainWindow.config.items('RoomsStatus')[0][0]
        self.preroomid = roomid
        self.ui.roomid.setText(roomid)

    def danmaku_printtext(self, text):
        self.ui.danmaku.append(text)

    def gift_printtext(self, text):
        self.ui.gifts.append(text)

    def cookie_window(self):
        self.cookie_window = cookie_widget()
        self.cookie_window.ui.show()


def reboot():
    # 获取当前解释器路径
    p = sys.executable
    # 启动新程序(解释器路径, 当前程序)
    os.execl(p, p, *sys.argv)
    # # 关闭当前程序
    # sys.exit()


if __name__ == '__main__':
    App = QApplication(sys.argv)  # 创建QApplication对象，作为GUI主程序入口
    mainw = MainWindow()
    mainw.ui.show()  # 显示主窗体
    sys.exit(App.exec_())
