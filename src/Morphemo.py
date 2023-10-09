# -*- coding: UTF-8 -*-
"""
-*- Coded by LLK -*-\n
Morphemo 类为主类，用于调用其他类的方法。
"""

import os
import sys
import platform
from Crawler import MorphemoCrawler
from PySide6 import QtCore, QtGui
from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QUrl)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QMainWindow, QSizePolicy, QWidget)

if platform.system() == 'Windows':
  filePath = 'file:///' + '/'.join(os.path.dirname(os.path.abspath(__file__)).split('\\')) + '/pages/index.html'
else:
  filePath = 'file:///' + os.path.dirname(os.path.abspath(__file__)) + '/pages/index.html'


class Ui_Mophemo(object):
    def setupUi(self, Mophemo):
        if not Mophemo.objectName():
            Mophemo.setObjectName(u"Mophemo")
        Mophemo.resize(712, 554)
        self.centralwidget = QWidget(Mophemo)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.webEngineView = QWebEngineView(self.centralwidget)
        self.webEngineView.setObjectName(u"webEngineView")
        self.webEngineView.setGeometry(QRect(0, 0, 711, 551))
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.webEngineView.sizePolicy().hasHeightForWidth())
        self.webEngineView.setSizePolicy(sizePolicy1)
        self.webEngineView.setToolTipDuration(-1)
        self.webEngineView.setUrl(QUrl(filePath))
        Mophemo.setCentralWidget(self.centralwidget)

        self.retranslateUi(Mophemo)

        QMetaObject.connectSlotsByName(Mophemo)
    # setupUi

    def retranslateUi(self, Mophemo):
        Mophemo.setWindowTitle(QCoreApplication.translate("Mophemo", u"MainWindow", None))
    # retranslateUi


def main():
  app = QApplication(sys.argv)
  mw = QMainWindow()
  obj = Ui_Mophemo()
  icon = QtGui.QIcon()
  icon.addPixmap(QtGui.QPixmap("assets/TChub.ico"))  # 设置图标
  mw.setWindowIcon(icon)
  obj.setupUi(mw)
  mw.show()
  sys.exit(app.exec())


if __name__ == '__main__':
  main()
