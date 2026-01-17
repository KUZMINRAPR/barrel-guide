import time
import os
from OrangeGPIO import OrangeGPIO

PINS = {
    "L_A": OrangeGPIO("I0"), # 29 pin
    "L_B": OrangeGPIO("I15") # 31 pin
}

# Экспортируем и настраиваем все пины
for name, pin in PINS.items():
    pin.export()            # ПОТОМ экспортируем
    pin.set_direction("in")

last = {name: pin.read() for name, pin in PINS.items()}

print("ENC CHECK: GPIO с pull-down резисторами")
print("Ctrl+C для выхода.\n")

try:
    while True:
        changed = False
        for name, pin in PINS.items():
            v = pin.read()
            if v != last[name]:
                changed = True
                last[name] = v
                print(f"{time.time():.3f}  {name} (GPIO{pin}) = {v}")
        if not changed:
            time.sleep(0.01)
except KeyboardInterrupt:
    pass
finally:
    for name, pin in PINS.items():
        pin.unexport()
    print("GPIO cleaned up")