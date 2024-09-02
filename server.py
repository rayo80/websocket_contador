
from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
from autobahn.websocket import ConnectionRequest
import devices as dv

MONGO_URI = 'mongodb://localhost'
db_name = 'RomaDBgps'


class MyServerProtocol(WebSocketServerProtocol):
    """ Server para prueba de Contadores"""
    def __init__(self, fact):
        super().__init__()
        self.factory = fact
        self.device = dv.Contador()

    async def onConnect(self, request: ConnectionRequest):

        await self.device.conectar(request)
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    async def onMessage(self, payload, isBinary):
        if not isBinary:
            try:
                # Llamar al device
                value = await self.device.set_estado(payload)
                # Enviar de vuelta la suma acumulada
                self.sendMessage(str(value).encode('utf8'))
            except ValueError:
                # Manejar el caso en que no sea un número válido
                self.sendMessage(b"Please send a valid integer.")

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

    def onServerConnectionDropTimeout(self):
        print("WebSocket is connecting")


class MySocketServerFactory(WebSocketServerFactory):
    protocol = MyServerProtocol

    def __init__(self, uri):
        super().__init__(uri)

    def create_protocol(self):
        return MyServerProtocol(self)
