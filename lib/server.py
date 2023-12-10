from abc import ABC, abstractmethod
import socket
from helpers import DataParser

class AbstractEchoServer(ABC):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        self.buffer_size = 1024
        print(f"Server listening on {self.host}:{self.port}")

    def run(self):
        print('Server is running, waiting for a connection...')
        connection, client_address = self.server_socket.accept()
        print(f"Connection from {client_address}")
        try:
            self.handle_client(connection)
        finally:
            connection.close()

    def handle_client(self, connection):
        try:
            while True:
                data = connection.recv(self.buffer_size)
                if data:
                    payload = DataParser.DecodeData(data)
                    self.on_event(payload['command'], payload['data'])
                    connection.sendall(data)
                else:
                    print("No more data from client.")
                    break
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            connection.close()
        pass


    @abstractmethod
    def on_event(self, command, payload):
        pass

    def close(self):
        self.server_socket.close()
        print('Server closed.')

class EchoServer(AbstractEchoServer):
    def handle_client(self, connection):
        try:
            while True:
                data = connection.recv()
                if data:
                    print(f"Received {data.decode()}")
                    connection.sendall(data)
                else:
                    print("No more data from client.")
                    break
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            connection.close()

