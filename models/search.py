"""
Model for search object.
"""


class Search():
    """
    Create a search object
    with a date and url content.
    """

    def __init__(self, date:str, url_content:str) -> None:
        self.date = date
        self.url_content = url_content
