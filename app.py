#!/usr/bin/env python3

"""
Principal file
for execute the mininal web browser.
"""

from tkinter import Tk
from models.ui import UI
from helpers import config

if __name__ == '__main__':
    # creating the windows for create the ui
    window = Tk()

    ui = UI(window)
    ui.create_menu()
    ui.create_ui()

    window.mainloop()
