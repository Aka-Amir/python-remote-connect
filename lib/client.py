import socket
from lib.helpers.DataParser import DataParser
from lib.models.payload_model import PayloadModel

class EventClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to {self.host} on port {self.port}.")

    def send_message(self, event, message):
        try:
            # Send data
            data = PayloadModel().set_command(event).set_payload(message).pipe(DataParser.EncodeData).build()
            self.client_socket.sendall(data)

            # Waiting for full echo response
            amount_received = 0
            amount_expected = len(message)

            while amount_received < amount_expected:
                data = self.client_socket.recv(16)
                amount_received += len(data)
                print(f'Received: {data.decode()}')

        finally:
            self.close()

    def close(self):
        self.client_socket.close()
        print('Connection closed.')

