#!/usr/bin/env python3

"""
Python Script for install the dependencies.
"""

import os
import subprocess

WORKING_DIRECTORY = os.getcwd()
REQUIREMENTS_FILE_PATH = WORKING_DIRECTORY + '/requirements.txt'


def pip_is_installed() -> bool:
    """
    Return True if pip is installed.
    """
    try:
        import pip
        return True

    except ImportError:
        return False


if __name__ == '__main__':
    print('\n----------- [+] Installing Minimal Web Browser -----------\n')

    pip_is_installed = pip_is_installed()

    # validating if pip package manager is installed
    if pip_is_installed:
        print('\n----------- [+] Installing Dependencies -----------\n')

        # in case pip3 not is a valid command try with pip command only
        try:
            subprocess.call(['pip3', 'install', '-r', REQUIREMENTS_FILE_PATH])
            print('\n----------- [+] Finish -----------\n')
        except FileNotFoundError:
            subprocess.call(['pip', 'install', '-r', REQUIREMENTS_FILE_PATH])
            print('\n----------- [+] Finish -----------\n')
    else:
        print('\n----------- [-] Pip package manager not is installed -----------\n')
