'''
This module is responsible for
building layout for GUI Tkinter
sniffer application. It contains
AppLayout class.
'''


import tkinter as tk
from tkinter import ttk


class AppLayout:
    '''
    AppLayout allows to build
    the whole interface in one
    place and store information
    about all the widgets in one
    object.
    Later this object should be
    passed to logic controller
    of the layout.
    '''

    window: tk.Tk
    start_button: ttk.Button
    stop_button: ttk.Button
    toggle_button: ttk.Button
    status_label: ttk.Label
    packets_list: ttk.Treeview

    def build(self) -> None:
        self._build_window()
        self._build_controls()
        self._build_packets_list()

    def _build_window(self) -> None:
        self.window = tk.Tk()
        self.window.title('Sniffer')
        self.window.geometry('800x600')

    def _build_controls(self) -> None:
        controls_frame = ttk.Frame(self.window)
        self.start_button = ttk.Button(controls_frame, text='Start')
        self.stop_button = ttk.Button(controls_frame, text='Stop')
        self.toggle_button = ttk.Button(controls_frame, text='Toggle')
        btns = [self.start_button, self.stop_button, self.toggle_button]
        for button in btns:
            button.pack(side=tk.LEFT)
        self.status_label = ttk.Label(controls_frame, text='Off')
        self.status_label.pack(side=tk.LEFT)
        controls_frame.pack(side=tk.TOP, fill='x')

    def _build_packets_list(self) -> None:
        ...
