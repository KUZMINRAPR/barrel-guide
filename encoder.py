from gpio import GPIO
import time
import threading

class Encoder(threading.Thread):
    def __init__(self, pins: dict):
        super().__init__()
        self._stop_event = threading.Event()
        self.pins = pins
        self.last = {name: pin.read() for name, pin in self.pins.items()}
        self.lock = threading.Lock()
        self.ticks = 0
    
    def get_ticks(self):
        with self.lock:
            return self.ticks
    
    def run(self):
        self.last = {name: pin.read() for name, pin in self.pins.items()}
        while not self._stop_event.is_set():
            for name, pin in self.pins.items():
                if self.last[name] != pin.read():
                    with self.lock:
                        self.ticks += 1
                    self.last[name] = pin.read()
            time.sleep(0.001)