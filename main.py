import time
from gpio import GPIO
from driver import Driver
from motor import Motor
from encoder import Encoder
import math

PINS = {
    "L_A": GPIO(17), # 11 pin
    "L_B": GPIO(27), # 13 pin
    "R_A": GPIO(22), # 15 pin
    "R_B": GPIO(9)  # 37 pin
}

DRIVER_PINS_IN = {"EN": GPIO(6), "INA": GPIO(13), "INB": GPIO(19), "PWMA": GPIO(26)}
DRIVER_PINS_OUT = {"A": GPIO(5), "B": GPIO(7)}

WHEEL_DIAMETER = 0.5 # В метрах
ENCODER_PPR = 2 # Импульсов за оборот
# GEAR_RATIO = 48 # Передаточное число редуктора

MOTOR_SPEED = 10000

TICKS_PER_REV = ENCODER_PPR # * GEAR_RATIO
print(f"Всего оборотов: {TICKS_PER_REV}")
WHEEL_CIRCUMFERENCE = math.pi * WHEEL_DIAMETER
print(f"Длина колеса: {WHEEL_CIRCUMFERENCE}")
TICKS_PER_METER = TICKS_PER_REV / WHEEL_CIRCUMFERENCE
print(f"Тиков за метр: {TICKS_PER_METER}")
DISTANCE = 3
TOTAL_TICKS = int(DISTANCE * TICKS_PER_METER)
print(f"Всего нужно тиков: {TOTAL_TICKS + 1}")


# Экспортируем и настраиваем все пины
for name, pin in PINS.items():
    pin.export()            
    pin.set_direction("out")

for name, pin in DRIVER_PINS_IN.items():
    pin.export()
    pin.set_direction("out")

for name, pin in DRIVER_PINS_OUT.items():
    pin.export()
    pin.set_direction("out")

driver = Driver(DRIVER_PINS_IN, DRIVER_PINS_OUT)
driver.state = "forward"
encoder = Encoder(PINS)
motor = Motor(driver, MOTOR_SPEED,encoder)

TICK_TIME = 3600 / motor.speed # Время одного тика

print("ENC CHECK: GPIO с pull-down резисторами")
print("Ctrl+C для выхода.\n")

try:
    counter = 0
    while counter < TOTAL_TICKS + 1:
        motor.run()
        if (encoder.tick()):
            counter += 1
            print(f"Счетчик: {counter}")
        time.sleep(TICK_TIME)
except KeyboardInterrupt:
    pass
finally:
    for name, pin in PINS.items():
        pin.unexport()
    print("GPIO cleaned up")