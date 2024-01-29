import socketserver
import io
import logging
import time
import numpy as np
import PIL
import PIL.Image
from threading import Condition, Thread, Event

class FalseCamera:
    def __init__(self, w=1024, h=768):
        self.w, self.h = self.size = w, h

    def capture(self, buf, format):
        while True:
            array = np.uint8(np.random.rand(self.h, self.w, 3)*256)
            im_pil = PIL.Image.fromarray(array)
            im_pil.save(buf, format=format)

            if self.event.is_set():
                break

    def start_recording(self, buf, format="jpeg"):
        self.t = Thread(target=self.capture, args=(buf, format))
        self.event = Event()
        self.t.start()

    def close(self):
        if self.t:
            self.event.set()
            self.t.join()

class StreamingOutput:
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # Ha començat un nou frame
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

