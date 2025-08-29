from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer
# from MainWindowUI import Ui_MainWindow
from ui_py.PiezoWidgetUI import Ui_PiezoWidget

import serial.tools.list_ports
from devices.PiezoStage import PiezoStage

class PiezoWidget(QWidget, Ui_PiezoWidget):
    def __init__(self, *args, obj=None, **kwargs):
        super(PiezoWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setupSignals()

        self.Stage_A = PiezoStage()
        self.Stage_B = PiezoStage()
        self.piezo_ports = []

        self.com_ports = serial.tools.list_ports.comports()
        self.com_options = []
        for port, desc, hwid in sorted(self.com_ports):
            self.com_options.append({'port': port, 'desc': desc})
        
        if len(self.com_options) > 1:
            for option in self.com_options:
                self.comPortComboA.addItem(f'{option["port"]}: {option["desc"]}')
                self.comPortComboB.addItem(f'{option["port"]}: {option["desc"]}')

            self.comPortComboA.setCurrentIndex(0)
            self.comPortComboB.setCurrentIndex(1)


    def setupSignals(self):        
        # Connect piezo stage button
        self.connectA.clicked.connect(lambda: self.stage_connect(self.Stage_A, self.piezo_ports[0]['port']))
        self.connectB.clicked.connect(lambda: self.stage_connect(self.Stage_B, self.piezo_ports[1]['port']))

        # Timer for displaying voltages
        self.voltage_timer=QTimer()
        self.voltage_timer.timeout.connect(self.update_voltages)

        # Timers for grounding
        self.x_timer_a=QTimer()
        self.y_timer_a=QTimer()
        self.z_timer_a=QTimer()
        self.x_timer_b=QTimer()
        self.y_timer_b=QTimer()
        self.z_timer_b=QTimer()

        # Connecting grounding buttons
        self.xGround_a_2.clicked.connect(lambda: self.x_timer_a.start(1000))
        self.yGround_a.clicked.connect(lambda: self.y_timer_a.start(1000))
        self.zGround_a.clicked.connect(lambda: self.z_timer_a.start(1000))
        self.xGround_b.clicked.connect(lambda: self.x_timer_b.start(1000))
        self.yGround_b.clicked.connect(lambda: self.y_timer_b.start(1000))
        self.zGround_b.clicked.connect(lambda: self.z_timer_b.start(1000))
        
    def stage_connect(self, controller, port):
        try:
            controller.connect(port)
            self.voltage_timer.start(250)

            if controller is self.Stage_A:
                self.connectA.setText('Disconnect')
                self.connectLabel_a.setText('A: connected')
                self.connectA.disconnect()
                self.connectA.clicked.connect(lambda: self.stage_disconnect(controller))

                self.xDisplay_a.setText(f'X: {controller.get_voltage("x")} V')
                self.xChange_a.setValue(controller.get_voltage('x'))

                self.yDisplay_a.setText(f'Y: {controller.get_voltage("y")} V')
                self.yChange_a.setValue(controller.get_voltage('y'))

                self.zDisplay_a.setText(f'Z: {controller.get_voltage("z")} V')
                self.zChange_a.setValue(controller.get_voltage('z'))
                
                self.xChange_a.valueChanged.connect(lambda: controller.set_voltage('x', self.xChange_a.value()))
                self.yChange_a.valueChanged.connect(lambda: controller.set_voltage('y', self.yChange_a.value()))
                self.zChange_a.valueChanged.connect(lambda: controller.set_voltage('z', self.zChange_a.value()))

                self.x_timer_a.timeout.connect(lambda: self.ground_voltage(controller, self.x_timer_a, 'x', self.xChange_a))
                self.y_timer_a.timeout.connect(lambda: self.ground_voltage(controller, self.y_timer_a, 'y', self.yChange_a))
                self.z_timer_a.timeout.connect(lambda: self.ground_voltage(controller, self.z_timer_a, 'z', self.zChange_a))

            if controller is self.Stage_B:
                self.connectB.setText('Disconnect')
                self.connectLabel_b.setText('B: connected')
                self.connectB.disconnect()
                self.connectB.clicked.connect(lambda: self.stage_disconnect(controller))

                self.xDisplay_b.setText(f'X: {controller.get_voltage("x")} V')
                self.xChange_b.setValue(controller.get_voltage('x'))

                self.yDisplay_b.setText(f'Y: {controller.get_voltage("y")} V')
                self.yChange_b.setValue(controller.get_voltage('y'))

                self.zDisplay_b.setText(f'Z: {controller.get_voltage("z")} V')
                self.zChange_b.setValue(controller.get_voltage('z'))
                
                self.xChange_b.valueChanged.connect(lambda: controller.set_voltage('x', self.xChange_b.value()))
                self.yChange_b.valueChanged.connect(lambda: controller.set_voltage('y', self.yChange_b.value()))
                self.zChange_b.valueChanged.connect(lambda: controller.set_voltage('z', self.zChange_b.value()))

                self.x_timer_b.timeout.connect(lambda: self.ground_voltage(controller, self.x_timer_b, 'x', self.xChange_b))
                self.y_timer_b.timeout.connect(lambda: self.ground_voltage(controller, self.y_timer_b, 'y', self.yChange_b))
                self.z_timer_b.timeout.connect(lambda: self.ground_voltage(controller, self.z_timer_b, 'z', self.zChange_b))

        except:
            print(f'Unable to find device in {port}')
    
    def stage_disconnect(self, controller, port):
        if controller is self.Stage_A:
            self.connectA.setText('Connect')
            self.connectLabel_a.setText('A: not connected')
            self.xDisplay_a.setText(f'X: 0.0 V')
            self.yDisplay_a.setText(f'Y: 0.0 V')
            self.zDisplay_a.setText(f'Z: 0.0 V')
            self.connectA.disconnect()
            self.connectA.clicked.connect(lambda: self.stage_connect(controller, port))

        if controller is self.Stage_B:
            self.connectB.setText('Connect')
            self.connectLabel_b.setText('B: not connected')
            self.xDisplay_b.setText(f'X: 0.0 V')
            self.yDisplay_b.setText(f'Y: 0.0 V')
            self.zDisplay_b.setText(f'Z: 0.0 V')
            self.connectB.disconnect()
            self.connectB.clicked.connect(lambda: self.stage_connect(controller, port))

    def update_voltages(self):
        if self.connectLabel_a.text() == 'A: connected':
            try:
                self.xDisplay_a.setText(f'X: {self.Stage_A.get_voltage("x")} V')
                self.yDisplay_a.setText(f'Y: {self.Stage_A.get_voltage("y")} V')
                self.zDisplay_a.setText(f'Z: {self.Stage_A.get_voltage("z")} V')
            except Exception as e:
                self.voltage_timer.stop()
                self.errorMessageBox.setWindowTitle('STAGE A')
                self.errorMessageBox.setText(f'ERROR: STAGE A NOT RESPONDING \n {e}')
                self.errorMessageBox.exec_()
                # self.stage_disconnect_a()

        if self.connectLabel_b.text() == 'B: connected':
            try:
                self.xDisplay_b.setText(f'X: {self.Stage_B.get_voltage("x")} V')
                self.yDisplay_b.setText(f'Y: {self.Stage_B.get_voltage("y")} V')
                self.zDisplay_b.setText(f'Z: {self.Stage_B.get_voltage("z")} V')
            except Exception as e:
                self.voltage_timer.stop()
                self.errorMessageBox.setWindowTitle('STAGE B')
                self.errorMessageBox.setText(f'ERROR: STAGE B NOT RESPONDING \n {e}')
                self.errorMessageBox.exec_()
                # self.stage_disconnect_a()

    def ground_voltage(self, controller, timer, dim, spinbox):
        v = controller.get_voltage(dim)
        if v <= 1 and v >= 0:
            controller.set_voltage(dim, 0)
            spinbox.setValue(0.0)
            timer.stop()
        else:
            controller.set_voltage(dim, v-1)