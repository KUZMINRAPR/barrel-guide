class Driver:
    def __init__(self, pins_in: dict, pins_out: dict):
        self.pins_in = pins_in
        for _, pin in pins_in.items():
            pin.export()
            pin.set_direction("in")
        
        self.pins_out = pins_out  
        for _, pin in pins_out.items():
            pin.export()
            pin.set_direction("out")
        
        # Инициализация: все выходы LOW (по умолчанию)
        self._set_outputs(0, 0)
    
    def __del__(self):
        for _, pin in self.pins_out.items():
            pin.unexport()
    
    def run(self):

        if 'EN' not in self.pins_in or 'INA' not in self.pins_in or 'INB' not in self.pins_in or 'PWMA' not in self.pins_in:
            raise ValueError("Требуются пины: EN, INA, INB, PWMA")
        
        en = self.pins_in['EN'].read()
        ina = self.pins_in['INA'].read()
        inb = self.pins_in['INB'].read()
        pwm = self.pins_in['PWMA'].read()
        
        if en == 0:
            outa = 0
            outb = 0
        else:
            if ina == 1 and inb == 1:
                outa = 1
                outb = 1  # Brake to VCC (PWM не влияет)
            elif ina == 1 and inb == 0:
                outa = 1 if pwm == 1 else 0
                outb = 0
            elif ina == 0 and inb == 1:
                outa = 0
                outb = 1 if pwm == 1 else 0
            else:  # 0 0
                outa = 0
                outb = 0
        
        self._set_outputs(outa, outb)
    
    def _set_outputs(self, outa, outb):
        self.pins_out['A'].write(outa)
        self.pins_out['B'].write(outb)
