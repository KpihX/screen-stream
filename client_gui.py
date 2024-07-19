import socket
import io
from PIL import Image, ImageTk
import pygame
import tkinter as tk
from tkinter import ttk

FPS = 60  # Limite de rafraîchissement à 60 images par seconde

class ScreenShareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Share")
        
        self.pause = False
        self.stop = False
        
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.btn_frame = ttk.Frame(root)
        self.btn_frame.pack(fill=tk.X)
        
        self.pause_btn = ttk.Button(self.btn_frame, text="Pause", command=self.toggle_pause)
        self.pause_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.stop_btn = ttk.Button(self.btn_frame, text="Stop", command=self.stop_stream)
        self.stop_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 5001))
        
        # self.screen = None
        self.clock = pygame.time.Clock()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.after(100, self.receive_screenshot)
    
    def toggle_pause(self):
        self.pause = not self.pause
        self.pause_btn.config(text="Resume" if self.pause else "Pause")
    
    def stop_stream(self):
        self.stop = True
    
    def on_closing(self):
        self.stop = True
        self.root.destroy()
    
    def receive_screenshot(self):
        if self.stop:
            self.client_socket.close()
            return
        
        if not self.pause:
            try:
                size = int.from_bytes(self.client_socket.recv(4), 'big')
                print(f"Taille reçue : {size}")

                img_bytes = bytearray()
                
                while len(img_bytes) < size:
                    packet = self.client_socket.recv(4096)
                    if not packet:
                        break
                    img_bytes.extend(packet)
                    # print(f"Paquet reçu : {len(packet)} octets")
                
                img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
                print(f"Dimensions de l'image : {img.size}")
                
                # Redimensionner l'image pour qu'elle s'adapte à la taille de la fenêtre
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()
                img = img.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
                
                self.photo = ImageTk.PhotoImage(img)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
                print("Image affichée")
                
                # Envoyer un signal au serveur pour indiquer que l'image a été reçue et traitée
                self.client_socket.sendall(b'1')
                
                # Limiter le taux de rafraîchissement
                self.clock.tick(FPS)
            
            except Exception as e:
                print(f"Erreur : {e}")
        
        self.root.after(100, self.receive_screenshot)

def main():
    root = tk.Tk()
    app = ScreenShareApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
