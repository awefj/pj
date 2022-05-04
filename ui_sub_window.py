# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_sub_window.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QListWidget,
    QListWidgetItem, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(500, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(500, 600))
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy1)
        self.frame.setMaximumSize(QSize(16777215, 50))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.progressBar = QProgressBar(self.frame)
        self.progressBar.setObjectName(u"progressBar")
        sizePolicy1.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy1)
        self.progressBar.setMinimumSize(QSize(0, 0))
        self.progressBar.setSizeIncrement(QSize(0, 0))
        self.progressBar.setLayoutDirection(Qt.LeftToRight)
        self.progressBar.setValue(0)
        self.progressBar.setAlignment(Qt.AlignJustify|Qt.AlignTop)
        self.progressBar.setOrientation(Qt.Horizontal)
        self.progressBar.setTextDirection(QProgressBar.TopToBottom)

        self.horizontalLayout.addWidget(self.progressBar)

        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.pushButton)


        self.verticalLayout.addWidget(self.frame)

        self.frame_3 = QFrame(Form)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.listWidget = QListWidget(self.frame_3)
        self.listWidget.setObjectName(u"listWidget")
        sizePolicy1.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy1)

        self.verticalLayout_3.addWidget(self.listWidget)

        self.listWidget_2 = QListWidget(self.frame_3)
        self.listWidget_2.setObjectName(u"listWidget_2")

        self.verticalLayout_3.addWidget(self.listWidget_2)

        self.widget = QWidget(self.frame_3)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton_2 = QPushButton(self.widget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_2.addWidget(self.pushButton_2)


        self.verticalLayout_3.addWidget(self.widget)


        self.verticalLayout.addWidget(self.frame_3)


        self.retranslateUi(Form)
        self.pushButton.clicked.connect(Form.cancel_btn_clicked)
        self.pushButton_2.clicked.connect(Form.delete_btn_clicked)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"Cancel", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"delete selected", None))
    # retranslateUi

