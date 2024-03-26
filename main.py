from app import run_application
from web import run_browser
from typing import Literal
import sys


def choose_app_form() -> Literal['app'] | Literal['web']:
    '''
    Chooses out of two options:
    1) app - run sniffer as a GUI app
    2) web - run sniffer in the web browser
    '''
    user_input: str
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
    else:
        user_input = input('How to run (web/app): ').strip()
    while user_input not in ['app', 'web']:
        user_input = input(f'Unknown option "{user_input}". Try again: ')
    return user_input


if __name__ == '__main__':
    form = choose_app_form()
    if form == 'app':
        run_application()
    else:
        run_browser()
