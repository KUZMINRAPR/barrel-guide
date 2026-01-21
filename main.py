import time
from gpio import GPIO
from driver import Driver
from motor import Motor
from encoder import Encoder
import math

ENCODER_PINS = {
    "L_A": GPIO(17), # 11 pin
    "L_B": GPIO(27), # 13 pin
    "R_A": GPIO(22), # 15 pin
    "R_B": GPIO(9),  # 37 pin
}
LEFT_DRIVER_PINS = {
    "EN": GPIO(6),   
    "INA": GPIO(13),
    "INB": GPIO(19),
    "PWMA": GPIO(26),
    "A": GPIO(5),
    "B": GPIO(7)
}
RIGHT_DRIVER_PINS = LEFT_DRIVER_PINS.copy() # TODO: Заполнить 

WHEEL_DIAMETER = 0.5 # В метрах
ENCODER_PPR = 2 # Импульсов за оборот
# GEAR_RATIO = 48 # Передаточное число редуктора

MOTOR_PWM = 1

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
for name, pin in ENCODER_PINS.items():
    pin.export()            
    pin.set_direction("out")

for name, pin in LEFT_DRIVER_PINS.items():
    pin.export()
    pin.set_direction("out")

for name, pin in RIGHT_DRIVER_PINS.items():
    pin.export()
    pin.set_direction("out")

encoders = {
    "left": Encoder({"A": ENCODER_PINS["L_A"], "B": ENCODER_PINS["L_B"]}),
    "right": Encoder({"A": ENCODER_PINS["R_A"], "B": ENCODER_PINS["R_B"]})
}

drivers = {
    "left": Driver(LEFT_DRIVER_PINS, state="forward"),
    "right": Driver(RIGHT_DRIVER_PINS, state="forward")
}

motors = {
    "left": Motor(drivers["left"], MOTOR_PWM, encoders["left"]),
    "right": Motor(drivers["right"], MOTOR_PWM, encoders["right"])
}

for encoder in encoders.values():
    encoder.start()
for motor in motors.values():
    motor.start()

print("ENC CHECK: GPIO с pull-down резисторами")
print("Ctrl+C для выхода.\n")

counter = 0
try:
    while counter < TOTAL_TICKS:
        counter = (encoders["left"].get_ticks() + encoders["right"].get_ticks()) // 2

        print(f"\nТики: {counter}/{TOTAL_TICKS}")

        if counter == TOTAL_TICKS:
            for motor in motors.values():
                motor.set("stop", 0)
            break

        time.sleep(0.001)
except KeyboardInterrupt:
    pass
finally:
    for m in motors.values():
        m._stop_event.set()
        m.join()
    for e in encoders.values():
        e._stop_event.set()
        e.join()
    for pin in ENCODER_PINS.values(): pin.unexport()
    for pin in LEFT_DRIVER_PINS.values(): pin.unexport()
    for pin in RIGHT_DRIVER_PINS.values(): pin.unexport()
    print("GPIO cleaned up")