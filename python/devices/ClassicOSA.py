import numpy as np
import pyvisa

class OSA:
    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        self.connected = False

    def connect(self):
        self.inst = self.rm.open_resource('GPIB0::1::INSTR')
        self.inst.clear()
        self.connected = True
        print('OSA connected')

    def disconnect(self):
        self.inst.close()

    def single_sweep(self):
        self.inst.query('SGL')
        self.inst.clear()

    def repeat_sweep(self):
        self.inst.query('RPT')
        self.inst.clear()

    def stop(self):
        self.inst.query('STP')
        self.inst.clear()

    def copy(self):
        self.inst.query('COPY1')
        self.inst.clear()
    
    def feed(self):
        self.inst.query('PRFED02')
        self.inst.clear()

    def get_spectrum(self):
        values = np.array(self.inst.query_ascii_values('LDATA'))
        self.inst.clear()
        return values[1:]
    
    def get_wavelength_range(self):
        start = self.inst.query('STAWL?').strip()
        stop = self.inst.query('STPWL?').strip()
        return [float(start), float(stop)]
    
    def set_start_wavelength(self, value: float):
        self.inst.query(f'STAWL{value}') 

    def set_stop_wavelength(self, value: float):
        self.inst.query(f'STPWL{value}')

    def set_auto_ref(self, value):
        if value:
            self.inst.query('ATREF1')
        else:
            self.inst.query('ATREF0')

    def is_auto_ref(self):
        m = self.inst.query('ATREF?').strip()
        if int(m) == 1:
            return True
        else:
            return False

    def get_resolution(self):
        return float(self.inst.query('RESLN?').strip())        

    def get_averaging(self):
        return int(self.inst.query('AVG?').strip())

    def set_averaging(self, value):
        self.inst.query(f'AVG{value:04}')

    def set_resolution(self, value: float):
        self.inst.query(f'RESLN{value}')

    def set_linear(self):
        self.inst.query('REFLU1.00')
        self.inst.query('REF=P')
        self.inst.clear()

    def set_log(self):
        self.inst.query('REFL004.0')
        self.inst.query('REF=P')
        self.inst.clear()

    def is_sweeping(self):
        m = self.inst.query('SWEEP?').strip()
        if m != '0':
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

# rm = pyvisa.ResourceManager()
# inst = rm.open_resource('GPIB0::1::INSTR')


# # inst.clear()
# # print(inst.query('*IDN?'))

# inst.query('REN')
# inst.query('EOI')

# inst.query('*RST')

# inst.query('RESLN1.00')
# rm.close()

# 
# # print(len(values[1:]))

# x = np.linspace(950, 1150, len(values)-1)
# plt.plot(x, values[1:])
# plt.show()

# inst.query('SGL')
# inst.query('LSCL0.10')
# inst.query('LSCL0')
# inst.query('REF=P')
# inst.query('ATREF0')
# inst.query('LSUNT0')

# inst.clear()
# inst.close()


A = OSA()
