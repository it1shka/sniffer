'''
This module is responsible for
controlling AppLayout instance
from the perspective of application's
logic
'''


from __future__ import annotations
from .layout import AppLayout


class AppLogic:
    '''Controls AppLayout'''

    layout: AppLayout

    def __init__(self, layout: AppLayout) -> None:
        self._layout = layout

    def bind(self) -> None:
        '''
        Attaches handlers to interactive components
        and initializes the logic part
        '''
        ...

    def run(self) -> None:
        '''Calls tkinter mainloop'''
        self._layout.window.mainloop()
