import pygame
import io
import sys
import os

from .watcher import CameraWatcher
from .config_io import ConfigIO

pygame.init()

FPS_UPDATE_EVT = pygame.event.custom_type()

class ImageVisualizers(pygame.sprite.Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class VisWindow(pygame.sprite.Sprite):
    """Visualization windows. They correspond to the physical areas
    where the images coming from the stream of the cameras are plotted.
    """
    def __init__(self, idx, size):
        super().__init__()

        self.idx = idx
        self.size = self.w, self.h = size

        # Image and rect, variables used to blit the image
        self.image = pygame.surface.Surface(size)
        self.rect = self.image.get_rect()

    def move(self, dr):
        self.rect.move_ip(dr)

    def update(self, camviewer):
        buf = camviewer.get_image(self.idx, timeout=1)
        self.image_stream = b''+ buf.getbuffer()
        # FIXME: This logic does not belong in here!!!!!
        if len(self.image_stream) == 0:
            return
            #raise ConnectionRefusedError
        full_image = pygame.image.load(buf, ".jpg").convert()
        pygame.transform.scale(full_image, self.size, dest_surface=self.image)

def load_stdin_data():
    # Ask for the ip addresses of the cameras
    while True:
        names = input("IP addresses of the cameras (space separated):\n> ")
        try:
            dirs = names.split(" ")
        except:
            print("I didn't get that...")
            continue
        break

    while True:
        disp = input("Set the disposition of the viewer (space separated):\n> ")
        try:
            geometry = disp.split(" ")
            geometry = [int(i) for i in geometry]
            cells = geometry[0] * geometry[1]
        except:
            print("I didn't get that...")
        if len(geometry) != 2:
            print("Bad geometry")
        elif geometry[0] * geometry[1] == len(dirs):
            break
        else:
            continue
    return {"geometry": geometry, "dirs": dirs}

class CameraViewer:
    def __init__(self, w, h, fullscreen=True):
        self.size = self.w, self.h = w, h

        self.config = ConfigIO()

        self.start()

        # Open the visualization window
        flags = 0
        if fullscreen:
            flags |= pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(self.size, flags=flags)

    def start(self):
        # Load from file if specified
        if len(sys.argv) == 2:
            try:
                fname = sys.argv[1]
                data = self.config.load(fname)
            except UnboundLocalError:
                pass
        else:
            data = load_stdin_data()

        geometry = data["geometry"]
        dirs = data["dirs"]
        self.n_cams = len(dirs)

        self.cams = CameraWatcher(self.n_cams)
        self.visualizers = ImageVisualizers()  # All visualizer surfaces are contained inside this group
        
        # Determining the size of each visualization window, in accordance with the display area
        vw, vh = self.w//geometry[1], self.h//geometry[0]
        for k in range(self.n_cams):
            # Init the connection
            self.cams.watch_camera((dirs[k], 8000))

            # Get the grid position of the visualizer
            i, j = k // geometry[1], k % geometry[0]
            # We create a visualization surface for each number of cameras connected!
            vis = VisWindow(k, (vw, vh))
            # We move the position of the visualizer to its corresponding space
            vis.move((vw*i, vh*j))
            # Finally, we add it to the group of visualizers
            self.visualizers.add(vis)
        
        self.images = [None for i in range(self.n_cams)]

        # Create a useful clock
        self.clock = pygame.time.Clock()

    def update_screen(self):
        self.visualizers.draw(self.screen)
        pygame.display.flip()

    def get_images(self):
        self.visualizers.update(self.cams)

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Save images
                    self.dump_images()
                if event.key == pygame.K_ESCAPE:
                    self.running= False
            if event.type == FPS_UPDATE_EVT:
                fps = self.clock.get_fps()
                pygame.display.set_caption(f"{fps:.3g} fps")


    def dump_images(self):
        viss = self.visualizers.sprites()
        for i, vis in enumerate(viss):
            with open(f"{i}.jpg", "wb") as imfile:
                data = vis.image_stream 
                imfile.write(data)

    def mainloop(self):
        self.running = True

        pygame.time.set_timer(FPS_UPDATE_EVT, 1000)
        while self.running:
            self.clock.tick()
            self.handle_events()

            # TODO: Check all works!!!!!!!
            self.get_images()

            self.update_screen()        

        self.close()

    def close(self):
        self.cams.close()
        pygame.quit()

    def __del__(self):
        try:
            self.close()
        except:
            pass
