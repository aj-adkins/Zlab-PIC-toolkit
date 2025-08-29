from PyQt6.QtWidgets import QWidget, QFileDialog, QColorDialog
import pyqtgraph as pg
import random

from ui_py.SpectrumWidgetUI import Ui_SpectrumWidget

class SpectrumWidget(QWidget, Ui_SpectrumWidget):
    def __init__(self, *args, obj=None, **kwargs):
        super(SpectrumWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setupSignals()

        self.plots_dict = {}

        self.setAcceptDrops(True)

    def setupSignals(self):
        self.addPlotButton.clicked.connect(self.add_plot)
        self.removePlotButton.clicked.connect(self.remove_plot)
        self.clearPlotButton.clicked.connect(self.clear_plot)
        self.colorButton.clicked.connect(self.set_plot_color)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            filename = url.toLocalFile()
            if filename:   # only handle real files
                self.load_plot(filename)

    def load_plot(self, filename):
        try:
            wavelength = []
            power = []
            with open(filename, 'r') as f:
                for line in f.readlines():
                    data_point = line.split()
                    wavelength.append(float(data_point[0]))
                    power.append(float(data_point[1]))
                
            self.graphWidget.showGrid(x=True, y=True, alpha=0.5)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            plot = pg.PlotCurveItem(x=wavelength, y=power, pen=color)
            self.graphWidget.addItem(plot)
            plot_name = filename.split('/')[-1]
            item = self.listWidget.addItem(plot_name)
            self.plots_dict[plot_name] = plot

        except:
            print('Invalid')

    def add_plot(self):
        filename, _ = QFileDialog.getOpenFileName()
        if filename:
            self.load_plot(filename)
        
        
    def remove_plot(self):
        current_item = self.listWidget.currentItem()
        self.graphWidget.removeItem(self.plots_dict[current_item.text()])
        self.listWidget.removeItemWidget(current_item)
        current_item.setHidden(True)
        
    def clear_plot(self):
        self.graphWidget.clear()
        self.listWidget.clear()

    def set_plot_color(self):
        color = QColorDialog.getColor()
        current_item = self.listWidget.currentItem()
        plot = self.plots_dict[current_item.text()]
        plot.setPen(color)