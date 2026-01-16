import time

class GPIO:
    def __init__(self, pin):
        self.pin = pin
        self.gpio_path = f"/sys/class/gpio/gpio{pin}"
        
    def export(self):
        try:
            with open("/sys/class/gpio/export", "w") as f:
                f.write(str(self.pin))
            time.sleep(0.1)  # Дать время системе создать файлы
        except IOError:
            print(f"GPIO {self.pin} уже экспортирован")
    
    def unexport(self):
        try:
            with open("/sys/class/gpio/unexport", "w") as f:
                f.write(str(self.pin))
        except IOError:
            print(f"GPIO {self.pin} больше не экспортирован")
    
    def set_direction(self, direction):
        """Установить направление: 'in' или 'out'"""
        with open(f"{self.gpio_path}/direction", "w") as f:
            f.write(direction)
    
    def write(self, value):
        """Записать значение: 1 (HIGH) или 0 (LOW)"""
        with open(f"{self.gpio_path}/value", "w") as f:
            f.write(str(value))
    
    def read(self):
        with open(f"{self.gpio_path}/value", "r") as f:
            return int(f.read().strip())

if __name__ == "__main__":
    pass