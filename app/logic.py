'''
This module is responsible for
controlling AppLayout instance
from the perspective of application's
logic
'''


from __future__ import annotations
from .layout import AppLayout
from scapy.all import *


class AppLogic:
    '''Controls AppLayout'''

    _layout: AppLayout
    _sniffer: AsyncSniffer

    def __init__(self, layout: AppLayout) -> None:
        self._layout = layout
        self._sniffer = AsyncSniffer(prn=self._process_packet, store=0)

    def bind(self) -> None:
        '''Attaches handlers to interactive components'''
        self._layout.start_button.config(command=self._handle_start)
        self._layout.stop_button.config(command=self._handle_stop)
        self._layout.toggle_button.config(command=self._handle_toggle)

    def run(self) -> None:
        '''Calls tkinter mainloop'''
        self._layout.window.mainloop()

    def _handle_start(self) -> None:
        if self._sniffer.running:
            return
        self._sniffer.start()
        self._layout.status_label.config(text='On')

    def _handle_stop(self) -> None:
        if not self._sniffer.running:
            return
        self._sniffer.stop()
        self._layout.status_label.config(text='Off')

    def _handle_toggle(self) -> None:
        if self._sniffer.running:
            self._handle_stop()
        else:
            self._handle_start()

    def _process_packet(self, packet: Packet) -> None:
        '''Processes packets from AsyncSniffer'''
        ...
