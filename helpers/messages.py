"""
Utils functions for
show messages in actions or other.
"""

from tkinter.messagebox import (
    showinfo,
    askquestion,
    showerror,
)
from tkinter.colorchooser import askcolor
from helpers.config import CONFIG_OBJECT

TITLE_UI = CONFIG_OBJECT['TITLE_UI']

def show_about() -> None:
    """
    Show the about message
    in the ui.
    """

    ABOUT_MESSAGE = '''
Minimal Web Browser is proyect made for Daniel Yanes using python3 with your tkinter module. For have a minimal web browser where see text and images only. No support javascript or css
    '''

    showinfo(TITLE_UI, ABOUT_MESSAGE)

def show_contact() -> None:
    """
    Show the contac message
    in the ui.
    """

    CONTACT_MESSAGE = '''
For contact to programmer use this email: eduarygp@gmail.com
    '''

    showinfo(TITLE_UI, CONTACT_MESSAGE)

def ask_if_exit() -> str:
    """
    Ask if the user want
    exit of the ui.
    """

    # asking
    response = askquestion(TITLE_UI, 'You want exit ?')

    return response


def show_cleaned_history(status:str) -> None:
    """
    Show a window with a success message
    when the history was cleaned. If there're
    some error show a error message.
    """

    if status == 'success':
        showinfo(TITLE_UI, 'History cleaned successfully')
    else:
        showerror(TITLE_UI, 'History no cleaned')


def show_copy_to_clipboard() -> None:
    """
    Show a window with a success message
    when the history text is copied to clipboard.
    """

    showinfo(TITLE_UI, 'History copied successfully')

def show_color_chooser() -> str:
    """
    Show a window for choose the
    color to set of the ui, and return
    the color choosed in hexadecimal format.
    """

    color_choosed = askcolor('#474E5E')[1]
    return color_choosed

def show_color_changed(new_color) -> None:
    """
    Show a window with a success message
    when the color of the ui is changed.
    """

    showinfo(TITLE_UI, f'Color changed to {new_color} successfully. Note: The changes is showed when the browser is open again')

def show_search_engine_changed(new_search_engine) -> None:
    """
    Show a window with a success message
    when the search engine is changed
    """

    showinfo(TITLE_UI, f'Search Engine changed to {new_search_engine} successfully. Note: The changes is showed when the browser is open again')
