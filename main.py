# -*- coding: UTF-8 -*- 
# Creator：LeK
# Date：2022/10/13


import sys
from PyQt5.QtWidgets import QApplication
from core import gui


if __name__ == '__main__':
    App = QApplication(sys.argv)  # 创建QApplication对象，作为GUI主程序入口
    mainw = gui.MainWindow()
    mainw.ui.show()  # 显示主窗体
    sys.exit(App.exec_())
