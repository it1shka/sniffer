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
        self._layout.clear_button.config(command=self._handle_clear)

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
        self._sniffer.stop(join=False)
        self._layout.status_label.config(text='Off')

    def _handle_toggle(self) -> None:
        if self._sniffer.running:
            self._handle_stop()
        else:
            self._handle_start()

    def _handle_clear(self) -> None:
        tree = self._layout.packets_list
        tree.delete(*tree.get_children())

    def _process_packet(self, packet: Packet) -> None:
        '''Processes packets from AsyncSniffer'''
        last_layer_name = packet.layers()[-1].__name__
        packet_title = f'{last_layer_name} packet'
        root = self._layout.packets_list.insert('', 'end', text=packet_title)
        self._insert_layers(root, packet)

    def _insert_layers(self, root: str, packet: Packet) -> None:
        for layer in packet.layers():
            title = layer.__name__
            layer_root = self._layout.packets_list.insert(root, 'end', text=title)
            for field_name in map(lambda e: e.name, layer.fields_desc):
                field_value = getattr(packet, field_name)
                self._layout.packets_list.insert(layer_root, 'end', text=field_name, values=(field_value,))
