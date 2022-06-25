"""
Utils functions to use.
"""

from json import load, dump
from json.decoder import JSONDecodeError
from requests import Request
from datetime import datetime
from models.search import Search
from data.layout_images import *
from .messages import *
from .config import CONFIG_OBJECT, CONFIG_FILE_PATH
import clipboard as cp
from pyperclip import PyperclipException


# path for the history file
HISTORY_FILE_PATH = './tmp/history.json'


def get_formated_url(url_content:str) -> str:
    """
    Return the url formated for make
    a query to a search engine.

    String to return:
        'word1+word2+word3+word4'
    """

    # save the result of the format
    url_formated = ''

    is_first_iteration = True
    for word in url_content.split():
        # validating is the first iteration
        if is_first_iteration:
            url_formated += word
            is_first_iteration = False
        else:
            url_formated += f'+{word}'
            is_first_iteration = False

    return url_formated



def get_valid_html(response:Request, url:str) -> str:

    # getting content_type
    content_type = response.headers['Content-Type']

    # validating if the file is a image to return
    if content_type == 'image/jpeg':
        html_content = LAYOUT_IMAGE.format(
            image_url = url
        )

    elif content_type == 'image/png':
        html_content = LAYOUT_IMAGE.format(
            image_url = url
        )

    # Not execute no tested. it's will be better if
    # is showed with a color
    # elif content_type == 'application/json':
        # json_dump = dumps(response.json(), indent = 2)
        # print(json_dump)
        # html_content = str(json_dump)

    else:
        html_content = str(response.text)

    return html_content


def get_history() -> dict:
    """
    Return the history object
    in the file './tmp/history.json'

    """

    # execption in case the file of history is empty
    try:
        # opening
        with open(HISTORY_FILE_PATH,'r') as f:
            HISTORY_OBJECT = load(f)
            f.close()

        return HISTORY_OBJECT

    except JSONDecodeError:
        return {}

def save_in_history(search:Search) -> None:
    """
    Save the search in the history file
    in './tmp/history.json'
    """

    # data to add of the file
    datetime_current = search.date
    url_content = search.url_content


    # execption is getted if the file is empty
    HISTORY_OBJECT = get_history()
    try:
        history_list = HISTORY_OBJECT['HISTORY']
        history_list.append({
            'dateTime': datetime_current,
            'url': url_content,
        })

        with open(HISTORY_FILE_PATH, 'w') as file:
            dump({
                'HISTORY': history_list,
            }, file, indent = 2)
            file.close()

    except KeyError:
        with open(HISTORY_FILE_PATH, 'w') as file:
            dump({
                'HISTORY': [{'dateTime': datetime_current, 'url': url_content}],
            }, file, indent = 2)

            file.close()


def clear_history() -> None:
    """
    Clear removing the content
    of the history file
    """

    try:
        # dumping the new file cleaned
        with open(HISTORY_FILE_PATH, 'w') as f:
            dump({
                'HISTORY': []
            }, f, indent = 2)
            f.close()

        show_cleaned_history('success')
    except:
        show_cleaned_history('error')


def copy_to_clipboard(to_copy:str) -> None:
    """
    Copy the text passed for parameter
    to the clipboard of the system.
    """

    # in case the copy of the selection
    # get a error
    try:
        cp.copy(to_copy)
        show_copy_to_clipboard()
    except PyperclipException:
        show_copy_to_clipboard()


def get_date_current() -> str:
    """
    Return the date and time
    current
    """

    # getting the current date and time
    datetime_current = datetime.now()
    datetime_current = datetime_current.strftime('%d/%m/%Y %H:%M:%S')

    return datetime_current


def change_value_in_config(value_to_change:str, new_value:str) -> None:
    """
    Change the value for the new value
    in the config file.
    """

    # validating the value to change
    if value_to_change == 'COLOR':
        # in case the color is None value
        if new_value == None:
            pass

        else:
            # assing new color
            CONFIG_OBJECT['COLOR_UI'] = new_value

            # dumping the file
            with open(CONFIG_FILE_PATH, 'w') as f:
                dump(CONFIG_OBJECT, f, indent = 2)
                f.close()

            show_color_changed(new_value)

    elif value_to_change == 'SEARCH_ENGINE':
        # assing new search engine
        CONFIG_OBJECT['SEARCH_ENGINE'] = new_value

        # dumping the file
        with open(CONFIG_FILE_PATH, 'w') as f:
            dump(CONFIG_OBJECT, f, indent = 2)
            f.close()

        show_search_engine_changed(new_value)
