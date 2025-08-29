import time
import numpy as np

from PyQt6.QtWidgets import QWidget, QFileDialog
from PyQt6.QtCore import QTimer

from devices.ClassicOSA import OSA
from devices.YokogawaOSA import YokogawaOSA

from ui_py.OSAWidgetUI import Ui_OSAWidget
from ui_py.SweepLoadingUI import Ui_sweepLoading


class OSAWidget(QWidget, Ui_OSAWidget):
    def __init__(self, *args, obj=None, **kwargs):
        super(OSAWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setupSignals()

    def setupSignals(self):
        # Connect OSA 
        self.osaConnectButton.clicked.connect(self.osa_connect)
        self.osaSweepButton.clicked.connect(self.osa_sweep)
        self.osaRepeatButton.clicked.connect(self.osa_repeat)
        self.osaSetLinButton.clicked.connect(self.set_linear)
        self.osaSetLogButton.clicked.connect(self.set_log)
        self.osaSaveButton.clicked.connect(lambda: self.save_osa_data(self.current_OSA_measurement))
        self.windowStartButton.clicked.connect(self.osa_window)

    def osa_connect(self):
        if self.classicOSAButton.isChecked():
            self.OSA = OSA()

            try:
                self.OSA.connect()
                self.osaConnectButton.setText('Disconnect')
                self.osaConnectButton.disconnect()
                self.osaConnectButton.clicked.connect(self.osa_disconnect)
                self.wavelengthStartEdit.setText(str(self.OSA.get_wavelength_range()[0]))
                self.wavelengthStopEdit.setText(str(self.OSA.get_wavelength_range()[1]))

            except Exception as e:
                print(f'OSA not found: {e}')

        elif self.yokoOSAButton.isChecked():
            self.OSA = YokogawaOSA()
            try:

                self.OSA.connect()
                self.osaConnectButton.setText('Disconnect')
                self.osaConnectButton.disconnect()
                self.osaConnectButton.clicked.connect(self.osa_disconnect)
                self.wavelengthStartEdit.setText(str(self.OSA.get_wavelength_range()[0]))
                self.wavelengthStopEdit.setText(str(self.OSA.get_wavelength_range()[1]))

            except Exception as e:
                print(f'OSA not found: {e}')

    def osa_disconnect(self):
        self.OSA.disconnect()
        print('OSA disconnected')
        self.osaConnectButton.setText('Connect')
        self.osaConnectButton.disconnect()
        self.osaConnectButton.clicked.connect(self.osa_connect)
    
    def osa_sweep(self):
        self.OSA.single_sweep()
        # loadingScreen.show()
        # loadingScreen.timer.start(750)

    def osa_repeat(self):
        # self.OSA.identify()
        self.osaRepeatButton.setText('Stop')
        self.osaRepeatButton.disconnect()
        self.osaRepeatButton.clicked.connect(self.osa_stop)
        # self.sweep_timer.start(1000)
        self.OSA.repeat_sweep()

    def osa_stop(self):
        self.osaRepeatButton.setText('Repeat')
        self.osaRepeatButton.disconnect()
        self.osaRepeatButton.clicked.connect(self.osa_repeat)
        # self.sweep_timer.stop()
        self.OSA.stop()
    
    def set_linear(self):
        self.OSA.set_linear()
        time.sleep(0.5)
        self.osa_measure()

    def set_log(self):
        self.OSA.set_log()
        time.sleep(0.5)
        self.osa_measure()

    def osa_measure(self):
        power = self.OSA.get_spectrum()
        wavelength_range = self.OSA.get_wavelength_range()
        wavelength = np.linspace(wavelength_range[0], wavelength_range[1], len(power))
        self.current_OSA_measurement = np.array([wavelength, power])
        self.plot_display(self.current_OSA_measurement)
        
    def plot_display(self, data):
        self.plotWidget.clear()
        self.plotWidget.showGrid(x=True, y=True, alpha=0.5)
        self.plotWidget.plot(data[0], data[1], pen='y')
        
    def save_osa_data(self, data):
        if self.OSA.connected:
            filename, _ = QFileDialog.getSaveFileName()
            with open(filename, 'a') as f:
                for i in range(len(data[0])):
                    f.write(f'{data[0][i]} {data[1][i]}\n')
        else:
            print('OSA not connected')

    def osa_window(self):
        num_windows = int(self.numWindowsSpin.value())

        if num_windows > 1:
            self.OSA.set_alarm(False)
            wavelength_range = self.OSA.get_wavelength_range()
            wavelength_span = wavelength_range[1] - wavelength_range[0]
            increment = wavelength_span/num_windows
            resolution = self.OSA.get_resolution()
            self.OSA.set_resolution(increment/1000)
            print(f'wavelength span: {wavelength_span}')
            print(f'increment: {increment}')
            print(f'resolution: {increment/1000}')

            data = []

            for i in range(num_windows):
                self.OSA.set_start_wavelength(wavelength_range[0] + i*increment)
                self.OSA.set_stop_wavelength(wavelength_range[0] + (i+1)*increment)
                self.OSA.single_sweep()

                time.sleep(1)

                # loadingScreen.show()
                # loadingScreen.timer.start(750)
                print(f'Running window sweep {i+1}')

                while self.OSA.is_sweeping():
                    time.sleep(1)
                
                power = self.OSA.get_spectrum()
                for val in power:
                    data.append(val)

            wavelength = np.linspace(wavelength_range[0], wavelength_range[1], len(data))
            self.plot_display(data=[wavelength, np.array(data)])

            if self.saveDataCheckbox.isChecked():
                filename, _ = QFileDialog.getSaveFileName()
                with open(filename, 'a') as f:
                    for i in range(len(data)):
                        f.write(f'{wavelength[i]} {data[i]}\n')

            time.sleep(1)
            self.OSA.set_start_wavelength(wavelength_range[0])
            self.OSA.set_stop_wavelength(wavelength_range[1])
            self.OSA.set_resolution(resolution)
            self.OSA.set_alarm(True)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

        else:
            print('Number of windows must be greater than one')

    
# class SweepLoading(QWidget, Ui_sweepLoading):
#     def __init__(self, *args, obj=None, **kwargs):
#         super(SweepLoading, self).__init__(*args, **kwargs)

#         self.setupUi(self) 
#         self.loading_state = 0
#         self.timer=QTimer()
#         self.timer.timeout.connect(self.loading)

#     def loading(self):
#             if self.loading_state == 3:
#                 self.label.setText('OSA sweeping ' + self.loading_state*'. ')
#                 self.loading_state = 0
#             else:
#                 self.label.setText('OSA sweeping ' + self.loading_state*'. ')
#                 self.loading_state += 1

#             if not OSA.is_sweeping():
#                 # osa.osa_measure()
#                 self.timer.stop()
#                 loadingScreen.hide()

