from interface import IDSCamera
import pygame

pygame.init()

def main():
    # Obrim la llibreria
    camera = IDSCamera()
    # Busquem dispositius disponibles
    camera.get_devices()
    # En seleccionem el primer
    camera.select_device(0)
    # Seleccionem els fps
    camera.set_fps(25)
    print(f"Capturing at {camera.get_fps():.4g} fps")
    # Seleccionem el temps d'exposició, en us
    camera.set_exposure_time(1000)
    print(f"Exposure: {camera.get_exposure_time():.4g} us")
    # Seleccionem la imatge de sortida
    camera.set_pixel_format("Mono8")
    # En mirem la resolució
    width, height = camera.get_resolution()
    print(f"Resoltion: {width}x{height}")
    # Comencem l'adquisició, que bloqueja canvis "crítics" en la càmera
    camera.start_acquisition()
    # Capturem imatges
    display = pygame.display.set_mode((1200, 900))
    disp_array = pygame.surfarray.pixels3d(display)
    running = True
    while running:
        image = camera.capture()
        reshapen = image.reshape((height, width))
        disp_array[:, :, 0] = reshapen[:900, :1200].T
        disp_array[:, :, 1] = reshapen[:900, :1200].T
        disp_array[:, :, 2] = reshapen[:900, :1200].T

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()

if __name__ == "__main__":
    main()
