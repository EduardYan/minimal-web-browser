"""
Utils functions for get
the configuration of the app.
"""

from json import load


CONFIG_FILE_PATH = './config.json'

class ConfigObjectInvalid(TypeError):
    """
    Model for the exception when
    the config object not is valid.
    """
    pass


def get_config_object() -> dict:
    """
    Return the config object
    in './config.json'.
    """

    # in case the config file not is found
    try:
        with open(CONFIG_FILE_PATH, 'r') as f:
            CONFIG_OBJECT = load(f)
            f.close()

        return CONFIG_OBJECT

    except FileNotFoundError:
        return {
            'TITLE_UI': 'Minimal Web Browser',
            'LOGO_PATH': './data/img/logo.png',
            'COLOR_UI': '#474E5E',
            'SEARCH_ENGINE': 'Google',
        }

def validate_config_object(config_object:dict) -> None:
    """
    Validate the config object passed
    for parameter, exeception is lauch
    when the config object not is valid.
    """


    # allows keys permited in the object
    ALLOWS_KEYS = [
        'TITLE_UI',
        'LOGO_PATH',
        'COLOR_UI',
        'SEARCH_ENGINE',
    ]

    for key in ALLOWS_KEYS:
        if not key in config_object:
            raise ConfigObjectInvalid(f'The config object of the file "{CONFIG_FILE_PATH}" not is valid.')

try:
    CONFIG_OBJECT = get_config_object()
    # validating the config object
    validate_config_object(CONFIG_OBJECT)

except ConfigObjectInvalid as error:
    print(f'\n----------- [-] {error} -----------\n')
    exit()
