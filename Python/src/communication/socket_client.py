import socket
import threading
from .constants import HOST, PORT


class SocketClient:
    def __init__(self, host=HOST, port=PORT):
        self.server_address = (host, port)
        self.socket = None
        self.connected = False
        self.lock = threading.Lock()

    def connect(self):
        """Establishes a TCP connection to the server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(self.server_address)
            self.connected = True
            print(f"Connected to UE at {self.server_address}")
        except Exception as e:
            print(f"Unable to connect to UE: {e}")
            self.connected = False

    def send_message(self, message):
        """Sends a JSON message to the server."""
        if self.connected:
            try:
                with self.lock:
                    self.socket.sendall((message + '\n').encode('utf-8'))
            except Exception as e:
                print(f"Error sending message: {e}")
                self.connected = False
                self.socket.close()

    def close(self):
        """Closes the socket connection."""
        if self.socket:
            self.socket.close()
            self.connected = False
            print("Socket connection closed.")
