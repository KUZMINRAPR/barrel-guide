import time
import os
from OrangeGPIO import OrangeGPIO

PINS = {
    "L_A": OrangeGPIO("I0"),   # pin 29
    "L_B": OrangeGPIO("I15"),   # pin 31
    "R_A": OrangeGPIO("I12"),   # pin 33
    "R_B": OrangeGPIO("I2"),   # pin 35
}


# Экспортируем и настраиваем все пины
for name, pin in PINS.items():
    pin.export()
    pin.set_direction("in")

last = {name: pin.read() for name, pin in PINS.items()}

print("ENC CHECK: смотрим уровни GPIO. Любое изменение будет напечатано.")
print("ВНИМАНИЕ: sysfs не поддерживает pull-down резисторы!")
print("Для теста проводом: кратко замкните нужный GPIO на 3.3V -> увидите 0->1->0.")
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
            time.sleep(0.01)  # 10 мс опрос
except KeyboardInterrupt:
    pass
finally:
    # Очистка: unexport всех пинов
    for name, pin in PINS.items():
        pin.unexport()
    print("GPIO cleaned up")
