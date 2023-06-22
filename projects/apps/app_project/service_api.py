import json, socket, os
from enum import Enum
from time import sleep

class ServiceType(Enum):
    NONE = 0
    DEPLOY = 1
    LOG = 2
    OFF = 3
    DELETE = 4

    def __str__(self) -> str:
        return self.name

    def get(typeService: str) -> 'ServiceType':
        if typeService == str(ServiceType.DEPLOY.name):
            return ServiceType.DEPLOY
        return ServiceType.NONE

class Service():
    def __init__(self):
        self.guid = ''
        self.type = ServiceType.NONE
        self.body = {}
        self.response = {}

    def from_json(self, data: str) -> None:
        self.guid = data['guid']
        self.type = ServiceType.get(data['type'])
        self.body = data['body']
        self.response = data['response']
    
    def to_json(self) -> str:
        return json.dumps(str({
            'guid': self.guid,
            'type': str(self.type),
            'body': self.body,
            'response': self.response
        }))

    def add_body(self, data: dict) -> 'Service':
        for k, v in data.items():
            self.body[k] = v
        return self

    def add_response(self, data: dict) -> 'Service':
        for k, v in data.items():
            self.response[k] = v
        return self


class ServiceApi():
    def __init__(self) -> None:
        self.service = Service()
    
    def send(self) -> str:
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_socket.connect((os.environ['HOST_NAME'], int(os.environ['PORT'])))
        sender_socket.settimeout(30)
        
        data = self.service.to_json()
        
        sender_socket.send(data.encode())
        response = sender_socket.recv(131072)
        sender_socket.close()

        response = eval(response)
        self.service.from_json(response)

