'''
Module contains static HTTP server
and websocket server
'''


from threading import Thread, Event
import http.server
import socketserver
import os
import websockets
from scapy.all import *


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
    _clients: set[websockets.WebSocketServerProtocol]

    def __init__(self, port: int) -> None:
        self._port = port
        self._clients = set()
        # TODO: instantiate sniffer

    def run(self) -> None:
        '''Starts the server'''
        # TODO: start the server
        print('Running websocket server...')