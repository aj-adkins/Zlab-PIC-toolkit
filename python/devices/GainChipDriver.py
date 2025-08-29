import serial 
import time

class GainChipDriver:
    def __init__(self):
        self.connected = False

    def open(self, port:str):
        self.ser = serial.Serial(port, baudrate=115200, timeout=1)
        if not self.ser.is_open:
            self.ser.open()
        self.connected = True
    
    def close(self):
        if self.ser.is_open:
            self.ser.close()
            self.connected = False

    def read_temp(self):
        self.ser.write(b'RDTA\r\n')
        response = self.ser.readline().decode()
        if 'READY' in response:
            return float(response.split("=", 1)[-1].strip())
        else:
            return 0.0

    def read_target_temp(self):
        self.ser.write(b'RDEA\r\n')
        response = self.ser.readline().decode()
        if 'READY' in response:
            return float(response.split("=", 1)[-1].strip())
        else:
            return 0.0

    
    def set_target_temp(self, value:float):
        self.ser.write(f'STEA{int(value*1000):06d}\r\n'.encode())
        
    def read_tec_state(self):
        self.ser.write(b'RDRA\r\n')
        response = self.ser.readline().decode()
        return int(response.split("=", 1)[-1].strip())
    
    def set_tec_state(self, state:int):
        self.ser.write(f'STRA00000{state}\r\n'.encode())

    def read_PID_P(self):
        self.ser.write(b'RDPA\r\n')
        response = self.ser.readline().decode()
        return float(response.split("=", 1)[-1].strip())
    
    def set_PID_P(self, value:float):
        self.ser.write(f'STPA{int(value*1000):06d}\r\n'.encode())

    def read_PID_I(self):
        self.ser.write(b'RDIA\r\n')
        response = self.ser.readline().decode()
        return float(response.split("=", 1)[-1].strip())
    
    def set_PID_I(self, value:float):
        self.ser.write(f'STIA{int(value*1000):06d}\r\n'.encode())
    
    def read_PID_D(self):
        self.ser.write(b'RDDA\r\n')
        response = self.ser.readline().decode()
        return float(response.split("=", 1)[-1].strip())
    
    def set_PID_D(self, value:float):
        self.ser.write(f'STDA{int(value*1000):06d}\r\n'.encode())
    
    
    def read_gain_current(self):
        try:
            self.ser.write(b'RDCA\r\n')
            response = self.ser.readline().decode()
            return float(response.split("=", 1)[-1].strip())
        except:
            return 0
    
    def set_gain_current(self, value:float):
        if value <= 600:
            self.ser.write(f'STCA{int(value*1000):06d}\r\n'.encode())
        else:
            print('Current too high!')
    
    def read_gain_state(self):
        self.ser.write(b'RDQA\r\n')
        response = self.ser.readline().decode()
        return int(response.split("=", 1)[-1].strip())
    
    def set_gain_state(self, state:int):
        self.ser.write(f'STQA00000{state}\r\n'.encode())

    def reset(self):
        self.ser.write(b'RST\r\n')
        self.ser.write(b'CLR\r\n')

