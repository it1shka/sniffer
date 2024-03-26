'''
This package is responsible
for running sniffer in browser
'''


from .server import run_static_server
from .server import WebSocketServer
from dotenv import load_dotenv
import os
import webbrowser


DEFAULT_STATIC_PORT = 3032
DEFAULT_WEBSOCKET_PORT = 4032


def get_ports() -> tuple[int, int]:
    '''
    Returns ports for
    1) static server
    2) websocket server
    '''
    static_port: int
    if 'STATIC_SERVER' in os.environ:
        static_port = int(os.environ['STATIC_SERVER'])
    else:
        static_port = DEFAULT_STATIC_PORT
    websocket_port: int
    if 'WS_SERVER' in os.environ:
        websocket_port = int(os.environ['WS_SERVER'])
    else:
        websocket_port = DEFAULT_WEBSOCKET_PORT
    return static_port, websocket_port


def run_browser() -> None:
    '''Will run browser version'''
    load_dotenv()
    static_port, websocket_port = get_ports()
    thread = run_static_server(static_port)
    server = WebSocketServer(websocket_port)
    server.run()
    webbrowser.open(f'localhost:{static_port}')
    thread.join()
