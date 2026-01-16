from gpio import GPIO
class OrangeGPIO(GPIO):
    def __init__(self, pin: str):
        super().__init__((ord(pin[0]) - 64 - 1) * 32 + int(pin[1:]))
    
    def export(self):
        return super().export()

    def unexport(self):
        return super().unexport()
    
    def set_direction(self, direction):
        return super().set_direction(direction)
    
    def read(self):
        return super().read()
    
    def write(self, value):
        return super().write(value)

if __name__ == "__main__":
    assert(OrangeGPIO("D12").pin == 108)
    assert(OrangeGPIO("A3").pin == 3)
    assert(OrangeGPIO("B11").pin == 43)
