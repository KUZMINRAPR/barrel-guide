from gpio import GPIO
import time

class Encoder:
    def __init__(self, pins: dict):
        self.pins = pins
        self.last = {name: pin.read() for name, pin in self.pins.items()}
    
    def tick(self):
        changed = False
        
        for name, pin in self.pins.items():
            v = pin.read()
            if v != self.last[name]:
                changed = True
                self.last[name] = v
                print(f"{time.time():.3f}  {name} (GPIO{pin}) = {v}")
        
        return changed