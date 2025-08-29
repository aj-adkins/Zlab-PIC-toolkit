from mdt69x import Controller
import time

class PiezoStage:
    def __init__(self):
        self.grounding_x = False

    def connect(self, port):
        self.c = Controller(port)

    def set_voltage(self, channel, val):
        if channel == 'x':
            self.c.set_x_voltage(val)
        if channel == 'y':
            self.c.set_y_voltage(val)
        if channel == 'z':
            self.c.set_z_voltage(val)

    def get_voltage(self, channel):
        if channel == 'x':
            return self.c.get_x_voltage()
        if channel == 'y':
            return self.c.get_y_voltage()
        if channel == 'z':
            return self.c.get_z_voltage()

        
    def ground_x(self):
        self.grounding_x = True
        xv = self.c.get_x_voltage()
        while xv > 0:
            if xv <= 1 and xv > 0:
                self.c.set_x_voltage(0)
                self.grounding_x = False
            else:
                self.c.set_x_voltage(xv - 1)
                xv = self.c.get_x_voltage()
                time.sleep(0.5)
        self.grounding_x = False

    def ground_y(self):
        yv = self.c.get_y_voltage()
        while yv > 0:
            if yv <= 1 and yv > 0:
                self.c.set_y_voltage(0)
                break
            else:
                self.c.set_y_voltage(yv - 1)
                yv = self.c.get_y_voltage()
                time.sleep(0.5)
    
    def ground_z(self):
        zv = self.c.get_z_voltage()
        while zv > 0:
            if zv <= 1 and zv > 0:
                self.c.set_z_voltage(0)
                break
            else:
                self.c.set_z_voltage(zv - 1)
                zv = self.c.get_z_voltage()
                time.sleep(0.5)

    def close(self):
        self.c.close()