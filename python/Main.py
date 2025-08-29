import sys
import copy 
import serial.tools.list_ports

from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QTimer, QPoint, Qt
from PyQt6.QtWidgets import QWidget, QFileDialog, QColorDialog, QMenu
import qdarktheme

from widgets.PiezoWidget import PiezoWidget
from widgets.SpectrumWidget import SpectrumWidget
from widgets.OSAWidget import OSAWidget
from widgets.GainChipWidget import GainChipWidget

from ui_py.MainWindowUI import Ui_MainWindow
from ui_py.WelcomeWidgetUI import Ui_WelcomeWidget

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle('Zlab PIC Toolkit')

        self.tabWidget.insertTab(0, WelcomeWidget(), '+')
    def setupSignals(self):
        self.tabWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tabWidget.customContextMenuRequested.connect(self.tab_menu)

    def tab_menu(self, pos: QPoint):
        menu = QMenu(self)
        close_action = menu.addAction('Close')
        close_all_action = menu.addAction('Close All')
        action = menu.exec(self.tabWidget.mapToGlobal(pos))

        if action == close_action:
            self.tabWidget.removeTab(self.tabWidget.currentIndex())
        if action == close_all_action:
            for i in range(self.tabWidget.count()-1):
                self.tabWidget.removeTab(0)

    def add_tab_menu(self, pos: QPoint):
        menu = QMenu(self)
        menu.addAction('OSA')
        menu.addAction('Piezo')
        menu.exec(self.tabWidget.mapToGlobal(pos))

class WelcomeWidget(QWidget, Ui_WelcomeWidget):
    def __init__(self, *args, obj=None, **kwargs):
        super(WelcomeWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.newPiezoButton.clicked.connect(self.add_new_piezo)
        self.newOSAButton.clicked.connect(self.add_new_osa)
        self.viewSpectrumButton.clicked.connect(self.add_new_spectrum)
        self.gainChipButton.clicked.connect(self.add_new_gain_chip)

    def add_new_piezo(self):
        tab_count = window.tabWidget.count()
        window.tabWidget.insertTab(tab_count-1, PiezoWidget(), 'Piezo')
        window.tabWidget.setCurrentIndex(tab_count-1)
        
    def add_new_osa(self):
        tab_count = window.tabWidget.count()
        window.tabWidget.insertTab(tab_count-1, OSAWidget(), 'OSA')
        window.tabWidget.setCurrentIndex(tab_count-1)

    def add_new_spectrum(self):
        tab_count = window.tabWidget.count()
        window.tabWidget.insertTab(tab_count-1, SpectrumWidget(), 'Spectrum')
        window.tabWidget.setCurrentIndex(tab_count-1)

    def add_new_gain_chip(self):
        tab_count = window.tabWidget.count()
        window.tabWidget.insertTab(tab_count-1, GainChipWidget(), 'Gain Chip')
        window.tabWidget.setCurrentIndex(tab_count-1)
        
app = QtWidgets.QApplication(sys.argv)
qdarktheme.setup_theme()
stylesheet = qdarktheme.setup_theme(corner_shape="sharp")

window = MainWindow()
welcome = WelcomeWidget()
window.setupSignals()
window.show()