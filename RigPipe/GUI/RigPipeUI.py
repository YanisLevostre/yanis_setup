
import sys

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLineEdit,
    QListWidget, QListWidgetItem, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(929, 819)
        #self.centralwidget = QWidget(MainWindow)
        #self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 891, 101))
        self.character_verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.character_verticalLayout.setObjectName(u"character_verticalLayout")
        self.character_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.character_lineEdit = QLineEdit(self.verticalLayoutWidget)
        self.character_lineEdit.setObjectName(u"character_lineEdit")

        self.character_verticalLayout.addWidget(self.character_lineEdit)

        self.selectCharacter_comboBox = QComboBox(self.verticalLayoutWidget)
        self.selectCharacter_comboBox.setObjectName(u"selectCharacter_comboBox")

        self.character_verticalLayout.addWidget(self.selectCharacter_comboBox)

        self.characterButtons_horizontalLayout = QHBoxLayout()
        self.characterButtons_horizontalLayout.setObjectName(u"characterButtons_horizontalLayout")
        self.characterSave_pushButton = QPushButton(self.verticalLayoutWidget)
        self.characterSave_pushButton.setObjectName(u"characterSave_pushButton")

        self.characterButtons_horizontalLayout.addWidget(self.characterSave_pushButton)

        self.characterLoad_pushButton = QPushButton(self.verticalLayoutWidget)
        self.characterLoad_pushButton.setObjectName(u"characterLoad_pushButton")

        self.characterButtons_horizontalLayout.addWidget(self.characterLoad_pushButton)


        self.character_verticalLayout.addLayout(self.characterButtons_horizontalLayout)

        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 120, 160, 651))
        self.modules_verticalLayout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.modules_verticalLayout.setObjectName(u"modules_verticalLayout")
        self.modules_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.module_lineEdit = QLineEdit(self.verticalLayoutWidget_2)
        self.module_lineEdit.setObjectName(u"module_lineEdit")

        self.modules_verticalLayout.addWidget(self.module_lineEdit)

        self.module_listWidget = QListWidget(self.verticalLayoutWidget_2)
        self.module_listWidget.setObjectName(u"module_listWidget")

        self.modules_verticalLayout.addWidget(self.module_listWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 929, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.character_lineEdit.setText(QCoreApplication.translate("MainWindow", u"character", None))
        self.characterSave_pushButton.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.characterLoad_pushButton.setText(QCoreApplication.translate("MainWindow", u"save", None))
        self.module_lineEdit.setText(QCoreApplication.translate("MainWindow", u"Modules", None))
    # retranslateUi


