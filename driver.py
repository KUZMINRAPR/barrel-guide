from gpio import GPIO
class Driver:
    def __init__(self, pins: dict, state="stop"):
        self.pins = pins
        self.state = state

        # Инициализация: все выходы LOW (по умолчанию)
        self._set_outputs(0, 0)
    
    def __del__(self):

        for _, pin in self.pins.items():
            pin.unexport()

    def forward(self):
        self.pins['EN'].write(1)
        self.pins['INA'].write(1)
        self.pins['INB'].write(0)
        self.pins['PWMA'].write(1)
        self.state = "forward"
    
    def backward(self):
        self.pins['EN'].write(1)
        self.pins['INA'].write(0)
        self.pins['INB'].write(1)
        self.pins['PWMA'].write(1)
        self.state = "backward"
    
    def run(self):

        if 'EN' not in self.pins or 'INA' not in self.pins or 'INB' not in self.pins or 'PWMA' not in self.pins:
            raise ValueError("Требуются пины: EN, INA, INB, PWMA")
        
        en = self.pins['EN'].read()
        ina = self.pins['INA'].read()
        inb = self.pins['INB'].read()
        pwm = self.pins['PWMA'].read()
        
        if en == 0:
            outa = 0
            outb = 0
        else:
            if ina == 1 and inb == 1:
                outa = 1
                outb = 1  # Brake to VCC (PWM не влияет)
                self.state = "stop"
            elif ina == 1 and inb == 0:
                outa = 1 if pwm == 1 else 0
                outb = 0
                self.state = "forward"
            elif ina == 0 and inb == 1:
                outa = 0
                outb = 1 if pwm == 1 else 0
                self.state = "backward"
            else:  # 0 0
                outa = 0
                outb = 0
                self.state = "stop"
        
        self._set_outputs(outa, outb)
    
    def _set_outputs(self, outa, outb):
        self.pins['A'].write(outa)
        self.pins['B'].write(outb)