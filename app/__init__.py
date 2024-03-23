'''
This package is responsible for
creation and management of Tkinter
GUI application for Sniffer
'''


from .layout import AppLayout
from .logic import AppLogic


def run_application() -> None:
    '''Will run Tkinter GUI sniffer'''
    layout = AppLayout()
    layout.build()
    logic = AppLogic(layout)
    logic.bind()
    logic.run()
