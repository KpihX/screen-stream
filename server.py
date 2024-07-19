#!/usr/bin/env python3
# -*-coding:UTF-8 -*
    
import socket
import os
import threading
import io
import sys

from dotenv import load_dotenv
from PIL import ImageGrab

# To load .env (common env vars)
load_dotenv()

# To load the .env.server (server env vars)
dotenv_path_server = os.path.join(os.path.dirname(__file__), '.env.server')
load_dotenv(dotenv_path=dotenv_path_server, override=True)

# Acces to environment variables
SERVER_ADDRESS = os.getenv('SERVER_ADDRESS')
SERVER_PORT = int(os.getenv('SERVER_PORT'))
MAX_CONNECTIONS = int(os.getenv('MAX_CONNECTIONS'))
MAX_SCREEN_SIZE = int(os.getenv('MAX_SCREEN_SIZE'))
MAX_SCREEN_BYTE_SIZE = int(os.getenv('MAX_SCREEN_BYTE_SIZE'))
MAX_CHUNK_SIZE=int(os.getenv("MAX_CHUNK_SIZE"))
CONTINUATION_SIGNAL=os.getenv("CONTINUATION_SIGNAL")

class ScreenStreamServer:
    def __init__(self, server_address=SERVER_ADDRESS, server_port=SERVER_PORT, max_connections=MAX_CONNECTIONS)-> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((server_address, server_port))
        self.socket.listen(max_connections)
        print("Server is running!")
        
        while True:
            client_socket, addr = self.socket.accept()
            print(f"Client connected: {addr}")
            threading.Thread(target=self.send_screenshot, args=(client_socket, addr)).start()

    def send_screenshot(self, client_socket:socket.socket, addr, max_screen_size=MAX_SCREEN_SIZE, max_screen_byte_size=MAX_SCREEN_BYTE_SIZE, max_chunk_size=MAX_CHUNK_SIZE, continuation_signal=CONTINUATION_SIGNAL):
        try:
            while True:
                img = ImageGrab.grab().convert('RGB')
                byte_arr = io.BytesIO()
                img.save(byte_arr, format='JPEG')
                img_bytes = byte_arr.getvalue()
                size = len(img_bytes)
                
                if size > max_screen_size:
                    print(f"Image size to big: {size} octets")
                    continue
                
                print(f"Sent image size: {size} octets")
                
                client_socket.sendall(size.to_bytes(max_screen_byte_size, 'big'))
                
                for i in range(0, size, max_chunk_size):
                    client_socket.sendall(img_bytes[i:i+max_chunk_size])

                # We wait for the client signal to send the next screenshot
                signal = client_socket.recv(1)
                
                if signal != continuation_signal.encode():      
                    print(f"Stopping of the sending!")
                    break
        except (BrokenPipeError, ConnectionResetError):
            print(f"!Client {addr} disconnected!", file=sys.stderr)
        except Exception as e:
            raise

def main():
    screen_stream_server = ScreenStreamServer()    
        
if __name__ == "__main__":
    main()
    
    input("\nGlad to have served you! Press 'Enter' to quit.")
    
