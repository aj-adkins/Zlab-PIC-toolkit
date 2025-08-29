import numpy as np
import pyvisa

class YokogawaOSA:
    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        self.connected = False

    def connect(self):
        self.inst = self.rm.open_resource('GPIB0::1::INSTR')
        self.inst.timeout = 30000
        self.inst.write('CFORM1')
        id = self.inst.query('*IDN?')
        print(f'{id} connected')
        self.connected = True
        
    def disconnect(self):
        self.inst.write('*GTL')
        self.inst.close()

    def single_sweep(self):
        self.inst.write(':init:smode 1')
        self.inst.write('*CLS')
        self.inst.write(':init')
        self.inst.clear()

    def repeat_sweep(self):
        self.inst.write(':init:smode 2')
        self.inst.write('*CLS')
        self.inst.write(':init')
        self.inst.clear()

    def stop(self):
        self.inst.write(':abor')
        self.inst.clear()

    def copy(self):
        print('This OSA has no printer')
        print('please wait 5 seconds')

    def feed(self):
        pass
    
    def get_spectrum(self):
        values = np.array(self.inst.query_ascii_values(':trace:y? tra'))
        # print(values)
        self.inst.clear()
        return values[1:]
    
    def get_wavelength_range(self):
        start = self.inst.query(':sense:wavelength:start?').strip()
        stop = self.inst.query(':sense:wavelength:stop?').strip()
        return [float(start)*1e9, float(stop)*1e9]
    
    def set_start_wavelength(self, value: float):
        self.inst.query(f':sense:wavelength:start {value}nm') 

    def set_stop_wavelength(self, value: float):
        self.inst.query(f':sense:wavelength:stop {value}nm')

    def set_auto_ref(self, value):
        pass
        # if value:
        #     self.inst.query('ATREF1')
        # else:
        #     self.inst.query('ATREF0')

    def is_auto_ref(self):
        pass
        # m = self.inst.query('ATREF?').strip()
        # if int(m) == 1:
        #     return True
        # else:
        #     return False

    def get_resolution(self):
        return float(self.inst.query(':sense:bandwidth:resolution?').strip())*1e9    

    def get_averaging(self):
        return int(self.inst.query(':sense:average:count?').strip())

    def set_averaging(self, value):
        self.inst.write(f':sense:average:count {int(value)}')

    def set_resolution(self, value: float):
        self.inst.write(f':sense:bandwidth:resolution {float(value)}nm')

    def set_linear(self):
        self.inst.write(':display:trace:y1:spacing lin')
        self.inst.clear()

    def set_log(self):
        self.inst.write(':display:trace:y1:spacing log')
        self.inst.clear()

    def is_sweeping(self):
        m = self.inst.query(':status:operation:condition?').strip()
        if int(m) == 0:
            return True 
        else:
            return False
        

    def query(self, command: str):
        self.inst.query(command)

    def set_alarm(self, value):
        if value:
            self.inst.query('BZWRN1')
        else:
            self.inst.query('BZWRN0')

    def identify(self):
        print(self.inst.query('*IDN?'))

import time
# osa = Yokogawa_OSA()

# osa.connect()
# # time.sleep(1000)
# # osa.single_sweep()
# # print(osa.is_sweeping())
# # osa.stop()

# rm = pyvisa.ResourceManager()
# inst = rm.open_resource('GPIB0::1::INSTR')
# # print(type(inst.query_ascii_values(':trace:x? tra')))
# while True:
#     print(len(inst.query_ascii_values(':trace:y? tra')))
#     time.sleep(0.25)

# inst.write(':stat:oper:even?')
# print(type(inst.read().strip()))
