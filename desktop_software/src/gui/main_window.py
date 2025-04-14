# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sheetsavvy_main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QListView, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QWidget)

class MainWindow(object):
    def setupUi(self, sheetsavvy_main_window):
        if not sheetsavvy_main_window.objectName():
            sheetsavvy_main_window.setObjectName(u"sheetsavvy_main_window")
        sheetsavvy_main_window.resize(552, 333)
        self.centralwidget = QWidget(sheetsavvy_main_window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.save_file_image_label = QLabel(self.centralwidget)
        self.save_file_image_label.setObjectName(u"save_file_image_label")

        self.gridLayout.addWidget(self.save_file_image_label, 0, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.reset_button = QPushButton(self.centralwidget)
        self.reset_button.setObjectName(u"reset_button")

        self.horizontalLayout.addWidget(self.reset_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.save_button = QPushButton(self.centralwidget)
        self.save_button.setObjectName(u"save_button")

        self.gridLayout.addWidget(self.save_button, 2, 1, 1, 1)

        self.device_info_list = QListView(self.centralwidget)
        self.device_info_list.setObjectName(u"device_info_list")

        self.gridLayout.addWidget(self.device_info_list, 0, 0, 1, 1)

        self.gridLayout.setColumnStretch(0, 200)
        self.gridLayout.setColumnStretch(1, 100)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        sheetsavvy_main_window.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(sheetsavvy_main_window)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 552, 33))
        sheetsavvy_main_window.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(sheetsavvy_main_window)
        self.statusbar.setObjectName(u"statusbar")
        sheetsavvy_main_window.setStatusBar(self.statusbar)

        self.retranslateUi(sheetsavvy_main_window)

        QMetaObject.connectSlotsByName(sheetsavvy_main_window)
    # setupUi

    def retranslateUi(self, sheetsavvy_main_window):
        sheetsavvy_main_window.setWindowTitle(QCoreApplication.translate("sheetsavvy_main_window", u"SheetSavvy", None))
        self.save_file_image_label.setText("")
        self.reset_button.setText(QCoreApplication.translate("sheetsavvy_main_window", u"Retry Connection", None))
        self.save_button.setText(QCoreApplication.translate("sheetsavvy_main_window", u"Save As", None))
    # retranslateUi

