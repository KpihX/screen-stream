import socket
import io
from PIL import Image
import pygame

NB_MAX_IMG = 20
FPS = 30  # Limite de rafraîchissement à 30 images par seconde

def receive_screenshot(client_socket):
    pygame.init()
    screen = None
    clock = pygame.time.Clock()
    
    # image_count = 0
    # while image_count < NB_MAX_IMG:  
    while True:
        try:
            size = int.from_bytes(client_socket.recv(4), 'big')
            print(f"Taille reçue : {size}")

            img_bytes = bytearray()
            
            while len(img_bytes) < size:
                packet = client_socket.recv(4096)
                if not packet:
                    break
                img_bytes.extend(packet)
                # print(f"Paquet reçu : {len(packet)} octets")
            
            img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
            print(f"Dimensions de l'image : {img.size}")
            
            if screen is None:
                screen = pygame.display.set_mode(img.size)
                print(f"Dimensions de la fenêtre Pygame : {img.size}")
            
            img_surface = pygame.image.fromstring(img.tobytes(), img.size, img.mode)
            screen.blit(img_surface, (0, 0))
            pygame.display.flip()
            print("Image affichée")
            
            # image_count += 1

            # Envoyer un signal au serveur pour indiquer que l'image a été reçue et traitée
            client_socket.sendall(b'1')
            
            # Limiter le taux de rafraîchissement
            clock.tick(FPS)
            
            # Gestion des événements Pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
        
        except Exception as e:
            print(f"Erreur : {e}")
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5001))
    receive_screenshot(client_socket)

if __name__ == '__main__':
    main()
