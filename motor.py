from driver import Driver
from encoder import Encoder
import time

class Motor:
    def __init__(self, driver: Driver, speed: int, encoder: Encoder):
        self.driver = driver
        self.speed = speed
        self.encoder = encoder
    
    def run(self):
        
        if self.driver.state == "forward":
            if self.encoder.pins["L_A"].read() == 0:
                self.encoder.pins["L_A"].write(1)
            else:
                self.encoder.pins["L_A"].write(0)
            
        elif self.driver.state == "backward":
            if self.encoder.pins["L_A"].read() == 0:
                self.encoder.pins["L_B"].write(1)
            else:
                self.encoder.pins["L_B"].write(0)
