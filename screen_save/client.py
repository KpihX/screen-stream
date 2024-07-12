import os
import socket
import io
from PIL import Image
import time

NB_MAX_IMG = 20

def receive_screenshot(client_socket, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    image_count = 0
    while image_count < NB_MAX_IMG:  
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
            
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            img_path = os.path.join(save_dir, f"screenshot_{timestamp}_{image_count}.png")
            img.save(img_path)
            print(f"Image sauvegardée à : {img_path}")
            
            image_count += 1

            # Envoyer un signal au serveur pour indiquer que l'image a été reçue et traitée
            client_socket.sendall(b'1')
        
        except Exception as e:
            print(f"Erreur : {e}")
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5001))
    save_dir = 'screenshots'
    receive_screenshot(client_socket, save_dir)

if __name__ == '__main__':
    main()
