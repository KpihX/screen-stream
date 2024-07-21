#!/usr/bin/env python3
# -*-coding:UTF-8 -*
    
import os
import tkinter as tk
import socket
import pygame
import io

from dotenv import load_dotenv
from tkinter import ttk
from PIL import Image, ImageTk

# To load .env (common env vars)
load_dotenv()

# To load the .env.client (client env vars)
client_path_dotenv = os.path.join(os.path.dirname(__file__), ".env.client")
load_dotenv(dotenv_path=client_path_dotenv, override=True)

FPS=int(os.getenv("FPS"))
CANVAS_HEIGHT=int(os.getenv("CANVAS_HEIGHT"))
CANVAS_WIDTH=int(os.getenv("CANVAS_WIDTH"))
SCREEN_ASK_DELAY=int(os.getenv("SCREEN_ASK_DELAY"))
MAX_SCREEN_BYTE_SIZE=int(os.getenv("MAX_SCREEN_BYTE_SIZE"))

SERVER_ADDRESS=os.getenv("SERVER_ADDRESS")
SERVER_PORT=int(os.getenv("SERVER_PORT"))
MAX_CHUNK_SIZE=int(os.getenv("MAX_CHUNK_SIZE"))
CONTINUATION_SIGNAL=os.getenv("CONTINUATION_SIGNAL")

class ScreenStreamFrame(tk.Frame):
    def __init__(self, master, server_adress=SERVER_ADDRESS, server_port=SERVER_PORT, canvas_width=CANVAS_WIDTH, canvas_heigth=CANVAS_HEIGHT, screen_ask_delay=SCREEN_ASK_DELAY)-> None:
        tk.Frame.__init__(self, master)
        self.master = master
        
        self.canvas = tk.Canvas(self.master, width=canvas_width, height=canvas_heigth)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.pause = False
        self.stop = False
        
        self.btn_frame = ttk.Frame(self.master)
        self.btn_frame.pack(fill=tk.X)
        
        self.pause_btn = ttk.Button(self.btn_frame, text="Pause", command=self.toggle_pause)
        self.pause_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.stop_btn = ttk.Button(self.btn_frame, text="Stop", command=self.stop_screen_stream)
        self.stop_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server_adress, server_port))
        
        self.clock = pygame.time.Clock()
        
        self.screen_ask_delay = screen_ask_delay
        self.master.after(self.screen_ask_delay, self.receive_screenshot)
    def toggle_pause(self)-> None:
        self.pause = not self.pause
        self.pause_btn.config(text="Resume" if self.pause else "Pause")

    def stop_screen_stream(self)-> None:
        self.stop = True
        if self.photo:
            del self.photo
        self.destroy()
        
    def receive_screenshot(self, max_screen_byte_size=MAX_SCREEN_BYTE_SIZE, max_chunk_size=MAX_CHUNK_SIZE, continuation_signal=CONTINUATION_SIGNAL, fps=FPS)-> None:
        if self.stop:
            self.socket.close()
            return
        
        if not self.pause:
            try:
                size = int.from_bytes(self.socket.recv(max_screen_byte_size), 'big')
                print(f"Received size: {size}")
                
                img_bytes = bytearray()
                
                while len(img_bytes) < size:
                    chunk = self.socket.recv(max_chunk_size)
                    if not chunk:
                        break
                    img_bytes.extend(chunk)
                    # print(f"Received chunk: {len(chunk)} Bytes.")
                    
                img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
                print(f"Received image size: {img.size}.")
                    
                # Redimensionning of the image
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()
                img = img.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
                    
                    
                self.photo = ImageTk.PhotoImage(img)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
                print("Image displayed!")
                    
                # Signal to ask for the next image
                self.socket.sendall(continuation_signal.encode())
                    
                # We limit the refreshing rate
                self.clock.tick(fps)
            except Exception as e:
                raise
            
            
        self.master.after(self.screen_ask_delay, self.receive_screenshot)
    
class ScreenStreamApp(tk.Frame):
    def __init__(self, master:tk.Tk) -> None:
        tk.Frame.__init__(self, master)
        self.screen_stream_frame = ScreenStreamFrame(self)
        self.screen_stream_frame.pack()
        
def main():
    root = tk.Tk() 
    app = ScreenStreamApp(root)
    app.pack()
    root.title("Screen Stream")
    root.mainloop()
    
if __name__ == '__main__':
    main()
    
    input("\nGlad to have served you! Press 'Enter' to quit.")
