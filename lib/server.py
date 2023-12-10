from abc import ABC, abstractmethod
import socket
from helpers import DataParser
from models.payload_model import PayloadModel

class AbstractEchoServer(ABC):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        self.buffer_size = 1024
        self.connection: socket.socket = None
        print(f"Server listening on {self.host}:{self.port}")

    def run(self):
        print('Server is running, waiting for a connection...')
        connection, client_address = self.server_socket.accept()
        print(f"Connection from {client_address}")
        try:
            #TODO: Create new thread for new connection inorder to handle async
            self.handle_client(connection)
        finally:
            connection.close()

    def handle_client(self, connection):
        try:
            self.connection = connection
            while True:
                data = connection.recv(self.buffer_size)
                if data:
                    payload = PayloadModel(as_dict=DataParser.DecodeData(data))
                    self.on_event(payload.command, payload.data)
                    ack_payload = PayloadModel().set_command('ack').pipe(DataParser.EncodeData)
                    connection.sendall(ack_payload.build())
                else:
                    print("No more data from client.")
                    break
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            connection.close()
        pass

    def send(self, data: PayloadModel):
        self.connection.sendall(data.build())



    @abstractmethod
    def on_event(self, command, payload):
        pass

    def close(self):
        self.server_socket.close()
        print('Server closed.')

class EventBaseServer(AbstractEchoServer):
    
    __subs__ = {}
    
    def on_event(self, command, payload):
        self.__subs__[command](payload)
    
    def subscribe(self, command, call_back):
        self.__subs__[command] = call_back

    def emit_data(self, command: str, payload: str):
        self.send(PayloadModel(command=command, payload=payload))
