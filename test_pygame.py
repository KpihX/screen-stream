import os
os.environ['SDL_VIDEODRIVER'] = 'directfb'
import pygame
from PIL import Image
import io

def display_test_image():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    img = Image.new('RGB', (800, 600), color = 'red')
    byte_arr = io.BytesIO()
    img.save(byte_arr, format='JPEG')
    img_bytes = byte_arr.getvalue()
    img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
    img_surface = pygame.image.fromstring(img.tobytes(), img.size, img.mode)
    screen.blit(img_surface, (0, 0))
    pygame.display.flip()
    print("Image de test affichée")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

display_test_image()
