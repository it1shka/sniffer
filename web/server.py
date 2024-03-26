'''
Module contains static HTTP server
and websocket server
'''


from threading import Thread, Event
import http.server
import socketserver
import os
import websockets as ws
import asyncio
from scapy.all import *
import json


def run_static_server(port: int) -> Thread:
    '''Serves /bundle directory'''
    started_event = Event()

    def _thread_handler() -> None:
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs) -> None:
                module_directory = os.path.dirname(__file__)
                static_directory = os.path.join(module_directory, 'bundle')
                super().__init__(*args, directory=static_directory, **kwargs)

            def do_GET(self) -> None:
                if self.path == '/':
                    self.path = '/index.html'
                super().do_GET()

        with socketserver.TCPServer(('', port), Handler) as httpd:
            started_event.set()
            httpd.serve_forever()

    server_thread = Thread(name='static-server', target=_thread_handler)
    server_thread.start()
    started_event.wait()
    return server_thread


class WebSocketServer:
    '''Instantiates ws server'''
    _port: int
    _sniffer: AsyncSniffer
    _clients: set[ws.WebSocketServerProtocol]

    def __init__(self, port: int) -> None:
        self._port = port
        self._clients = set()
        self._sniffer = AsyncSniffer(store=0, prn=self._process_packet)

    def _process_packet(self, packet: Packet) -> None:
        '''Processes packet from sniffer and broadcasts it'''
        layers = packet.layers()
        packet_title = layers[-1].__name__
        layers_info = {}
        for layer in layers:
            field_names = map(lambda e: e.name, layer.fields_desc)
            layer_info = {name: str(getattr(packet, name))
                          for name in field_names}
            layers_info[layer.__name__] = layer_info
        output = {
            'packet_title': packet_title,
            'layers': layers_info,
        }
        self._broadcast(json.dumps(output))

    def _broadcast(self, message: str) -> None:
        '''Broadcasts to all clients'''
        for socket in self._clients.copy():
            asyncio.run(WebSocketServer._send_message(socket, message))

    @staticmethod
    async def _send_message(socket: ws.WebSocketServerProtocol, message: str) -> None:
        '''Sends message to the websocket'''
        try:
            await socket.send(message)
        except ws.ConnectionClosed:
            pass

    async def _handle_socket(self, socket: ws.WebSocketServerProtocol) -> None:
        '''Handles connection lifetime'''
        self._clients.add(socket)
        try:
            await socket.wait_closed()
        finally:
            self._clients.remove(socket)

    async def _server_start(self) -> None:
        async with ws.serve(self._handle_socket, 'localhost', self._port):
            print('Websocket server started...')
            await asyncio.Future()

    def run(self) -> None:
        '''Starts both sniffer and server'''
        self._sniffer.start()
        print('Sniffer started...')
        ws_thread = Thread(
            name='web-socket',
            daemon=True,
            target=lambda: asyncio.run(self._server_start()),
        )
        ws_thread.start()
