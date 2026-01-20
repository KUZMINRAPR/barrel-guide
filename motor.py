from driver import Driver
from encoder import Encoder
import threading

class Motor(threading.Thread):
    def __init__(self, driver: Driver, pwm: float, encoder: Encoder, freq_hz=200):
        super().__init__()
        self.driver = driver
        self.pwm = pwm
        self.encoder = encoder
        self._stop_event = threading.Event()
        self.lock = threading.Lock()
        self.freq_hz = freq_hz
    
    def set(self, state:str, pwm:float):
        with self.lock:
            self.driver.state = state
            self.pwm = pwm

    def run(self):
        while not self._stop_event.is_set():
            if self.driver.state == "forward":
                if self.encoder.pins["A"].read() == 0:
                    self.encoder.pins["A"].write(1)
                    self.encoder.pins["B"].write(0)
                else:
                    self.encoder.pins["A"].write(0)
                    self.encoder.pins["B"].write(0)
            elif self.driver.state == "backward":
                if self.encoder.pins["B"].read() == 0:
                    self.encoder.pins["A"].write(0)
                    self.encoder.pins["B"].write(1)
                else:
                    self.encoder.pins["A"].write(0)
                    self.encoder.pins["B"].write(0)
            else:
                self.encoder.pins["A"].write(0)
                self.encoder.pins["B"].write(0)
