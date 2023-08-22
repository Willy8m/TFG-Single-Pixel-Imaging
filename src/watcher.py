import threading
import socket
import io

from .protocol import MsgProtocol, BUF_SIZE, CAM_RECV, TIMEOUT, CAM_SET_SHUTTER

class CameraWatcher(MsgProtocol):
    def __init__(self, n_cameras):
        self.conditions = [threading.Condition() for i in range(n_cameras)]

        self.images = [io.BytesIO() for i in range(n_cameras)]

        self.stop_event = threading.Event()

        self.cameras = {}

    def watch_camera(self, server, shutter_speed=None):
        n_cam = len(self.cameras)-1
        t = threading.Thread(target=self._watch_camera, args=(server,), kwargs={"shutter_speed":shutter_speed})
        self.cameras[n_cam] = t
        t.daemon = True
        t.start()

    def get_image(self, n_cam, timeout=None):
        with self.conditions[n_cam]:
            self.conditions[n_cam].wait(timeout=timeout)
            frame = self.images[n_cam]
        return frame

    def __set_shutter_speed(self, server, shutter_speed):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(TIMEOUT)
            sock.connect(server)
            
            # Commence server communication, asking for speed change
            self.send_bytes(sock, CAM_SET_SHUTTER)
            self.send_string(sock, str(shutter_speed))

    def _watch_camera(self, server, shutter_speed=None):
        n_cam = len(self.cameras)-1

        if shutter_speed:
            self.__set_shutter_speed(server, shutter_speed)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(TIMEOUT)
            sock.connect(server)
            
            # Commence server communication, asking for camera capture
            self.send_bytes(sock, CAM_RECV)
            while True:
                if self.stop_event.is_set():
                    break
            
                # Poll images
                image = self.receive_bytes(sock)
                # Convert to a BytesIO so that pygame can read them...
                with self.conditions[n_cam]:
                    self.images[n_cam] = io.BytesIO(image)
                    self.conditions[n_cam].notify_all()

    def get_connected_cameras(self):
        return len(self.cameras)

    def close(self):
        # Close all pending connections and sockets
        self.stop_event.set()
        for camera in self.cameras:
            # Kill all children
            t = self.cameras[camera]
            t.join()

    def __del__(self):
        self.close()
