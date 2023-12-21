import socket
from abc import ABC, abstractmethod

from lib.threading.task import Task
from lib.helpers.DataParser import DataParser
from lib.models.payload_model import PayloadModel
from lib.threading.task_manager import TaskManager

class EventClient(ABC):
    def __init__(self, host, port, buffer_size=1024):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to {self.host} on port {self.port}.")

    def send_message(self, event, message):
        try:

            data = PayloadModel().set_command(event).set_payload(message).pipe(DataParser.EncodeData).build()
            self.client_socket.sendall(data)

        except:
            print(message)

    def __listen__(self):
        task_manger = TaskManager()
        while True:
            data = self.client_socket.recv(self.buffer_size)
            payload = PayloadModel(as_dict=DataParser.DecodeData(data))
            if payload.command == 'ack':
                print('got ack')
                continue
            task_manger.start(Task(self.__event_publisher__, payload))

    def __event_publisher__(self, payload: PayloadModel):
        yield 'run'
        try:
            self.on_event(payload.command, payload.data)
            yield 'before'
            yield 'end'
        except:
            yield 'error'

    @abstractmethod
    def on_event(ev: str, data: str):
        pass

    def close(self):
        self.client_socket.close()
        print('Connection closed.')



class DefaultClient(EventClient):
    def __init__(self, host='0.0.0.0', port=3500, buffer_size=1024):
        super().__init__(host, port, buffer_size)
    
    __subs__ = {}
    
    def on_event(self, command, payload):
        if(self.__subs__[command] == None): return
        self.__subs__[command](payload)
    
    def subscribe(self, command, call_back):
        self.__subs__[command] = call_back

    def emit_data(self, command: str, payload: str):
        self.send_message(command, payload)
