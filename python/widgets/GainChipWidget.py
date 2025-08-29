import serial.tools.list_ports
import numpy as np

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPixmap

from devices.GainChipDriver import GainChipDriver

from ui_py.GainChipWidgetUI import Ui_GainChipWidget


class GainChipWidget(QWidget, Ui_GainChipWidget):
    def __init__(self, *args, obj=None, **kwargs):
        super(GainChipWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setupSignals()

        self.on_led = QPixmap("./graphics/on_led.png")
        self.on_led = self.on_led.scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.off_led = QPixmap("./graphics/off_led.png")
        self.off_led = self.off_led.scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        self.TECLED.setPixmap(self.off_led)
        self.laserLED.setPixmap(self.off_led)

        self.temp_timeseries = []
        # Set COM ports
        for port in list(serial.tools.list_ports.comports()):
            self.comComboBox.addItem(port.name, port)

        self.Controller = GainChipDriver()

    def setupSignals(self):
        self.readout_timer = QTimer()
        self.readout_timer.timeout.connect(self.display_temperature_current)

        self.plotting_timer = QTimer()
        self.plotting_timer.timeout.connect(self.plot_temp)

        self.comConnectButton.clicked.connect(self.connect_controller)
        self.setTECButton.clicked.connect(self.set_tec_params)
        self.enableTECButton.clicked.connect(self.enable_tec)
        self.laserEnableButton.clicked.connect(self.enable_laser)
        self.setCurrentButton.clicked.connect(self.set_laser_current)

    def connect_controller(self):
        try:
            # Connect to COM port and change connection buttons
            port = str(self.comComboBox.currentData().name)
            self.Controller.open(port)
            print(f'Succesfully connected to {self.comComboBox.currentData().description}')
            self.comConnectButton.setText('Disconnect')
            self.comConnectButton.disconnect()
            self.comConnectButton.clicked.connect(self.disconnect_controller)

            # Set parameter values 
            self.setTemperatureEdit.setText(str(self.Controller.read_target_temp()))
            self.PEdit.setText(str(self.Controller.read_PID_P()))
            self.IEdit.setText(str(self.Controller.read_PID_I()))
            self.DEdit.setText(str(self.Controller.read_PID_D()))
            # Start temperature readout
            self.readout_timer.start(100)

            # Check if TEC is already enabled
            if self.Controller.read_tec_state():
                self.enableTECButton.setText('Disable TEC')
                self.enableTECButton.clicked.disconnect()
                self.enableTECButton.clicked.connect(self.disable_tec)
                self.TECLED.setPixmap(self.on_led)

            # Start plotting
            self.plotting_timer.start(100)

        except Exception as e:
            print(e)
    
    def disconnect_controller(self):
        try:
            self.Controller.close()
            print('Disconnected controller')
            self.comConnectButton.setText('Connect')
            self.comConnectButton.disconnect()
            self.comConnectButton.clicked.connect(self.connect_controller)

            self.readout_timer.stop()
            self.tempReadout.setText('-')
            self.deviationLabel.setText('-')
            self.laserCurrentLabel.setText('-')
            self.setTemperatureEdit.clear()
            self.PEdit.clear()
            self.IEdit.clear()
            self.DEdit.clear()
            
    
        except Exception as e:
            print(e)

    def display_temperature_current(self):
        if self.Controller.connected:   
            self.tempReadout.setText(str(self.Controller.read_temp()))
            self.deviationLabel.setText(str(round(1000*(self.Controller.read_temp()-self.Controller.read_target_temp()), 3)))
            self.laserCurrentLabel.setText(str(self.Controller.read_gain_current()))

    def enable_tec(self):
        if self.Controller.connected:
            self.Controller.set_tec_state(1)
            self.enableTECButton.setText('Disable TEC')
            self.enableTECButton.clicked.disconnect()
            self.enableTECButton.clicked.connect(self.disable_tec)
            self.TECLED.setPixmap(self.on_led)

    def disable_tec(self):
        if self.Controller.connected:
            self.Controller.set_tec_state(0)
            self.enableTECButton.setText('Enable TEC')
            self.enableTECButton.clicked.disconnect()
            self.enableTECButton.clicked.connect(self.enable_tec)
            self.TECLED.setPixmap(self.off_led)

    def set_tec_params(self):
        if self.Controller.connected:
            self.Controller.set_target_temp(float(self.setTemperatureEdit.text()))
            # self.Controller.set_PID_P(float(self.PEdit.text()))
            # self.Controller.set_PID_I(float(self.IEdit.text()))
            # self.Controller.set_PID_D(float(self.DEdit.text()))

    def enable_laser(self):
        if self.Controller.connected:
            self.Controller.set_gain_state(1)
            self.laserEnableButton.setText('Disable Laser')
            self.laserEnableButton.clicked.disconnect()
            self.laserEnableButton.clicked.connect(self.disable_laser)
            self.laserLED.setPixmap(self.on_led)

    def disable_laser(self):
        if self.Controller.connected:
            self.Controller.set_gain_state(0)
            self.laserEnableButton.setText('Enable Laser')
            self.laserEnableButton.clicked.disconnect()
            self.laserEnableButton.clicked.connect(self.enable_laser)
            self.laserLED.setPixmap(self.off_led)

    def set_laser_current(self):
        if self.Controller.connected:
            self.Controller.set_gain_current(float(self.setCurrentEdit.text()))

    def plot_temp(self):
        if self.Controller.connected:
            if len(self.temp_timeseries) < 300:
                self.temp_timeseries.append(self.Controller.read_temp())
            else:
                self.temp_timeseries.append(self.Controller.read_temp())
                self.temp_timeseries = self.temp_timeseries[1:]
            self.TempPlot.clear()
            self.TempPlot.showGrid(x=True, y=True, alpha=0.5)
            x = np.array(range(len(self.temp_timeseries)))/10
            self.TempPlot.plot(x, self.temp_timeseries, pen='y')
            x_axis = self.TempPlot.getAxis('bottom')
            y_axis = self.TempPlot.getAxis('left')
            x_axis.setLabel('Time (s)')
            y_axis.setLabel('Temperature (C)')
