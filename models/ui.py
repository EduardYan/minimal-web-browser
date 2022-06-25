"""
This module have the model
for create a ui.
"""


from tkinter import (
    Tk,
    Frame,
    Label,
    Entry,
    Button,
    Menu,
    Toplevel,
    CENTER,
    PhotoImage,
)
from tkinter import ttk
from tkhtmlview import HTMLLabel
from requests import get
from requests.exceptions import (
    ConnectionError,
    ConnectTimeout,
    MissingSchema,
    InvalidSchema,
    InvalidURL,
)
import data.errors as err
import helpers.utils as ut
import helpers.config as conf
import helpers.messages as msn
from models.search import Search


class UI():
    """
    Create a ui object.

    Values default:
        TITLE_UI = 'Minimal Web Browser'
        LOGO_PATH = './data/img/logo.png'
        COLOR_UI = '#474E5E'
        SEARCH_ENGINE = 'google'
    """

    __CONFIG_OBJECT = conf.CONFIG_OBJECT

    TITLE_UI = __CONFIG_OBJECT['TITLE_UI']
    LOGO_PATH= __CONFIG_OBJECT['LOGO_PATH']
    # propertie no modificable outside of
    # the class
    __COLOR_UI = __CONFIG_OBJECT['COLOR_UI']

    # search engine to use
    SEARCH_ENGINE = __CONFIG_OBJECT['SEARCH_ENGINE']

    def __init__(self, window:Tk) -> None:
        self.wind = window
        # setting title
        self.wind.title(self.TITLE_UI)
        # setting the icon
        self.wind.tk.call('wm', 'iconphoto', self.wind._w, PhotoImage(file = self.LOGO_PATH))
        # setting the geometry
        self.wind.geometry('900x700')
        self.wind.config(bg = self.__COLOR_UI)

    def create_menu(self) -> None:
        """
        Create a bar menu in the
        top of the ui.
        """

        # creating principal menu
        self.bar_menu = Menu(
            self.wind,
            bg = '#222',
            fg = '#CCC',
            activebackground = '#333',
            activeforeground = '#CCC',
        )

        self.actions_menu = Menu(
            self.bar_menu,
            tearoff = 0,
            bg = '#666',
            fg = '#CCC',
            activebackground = '#777',
            activeforeground = '#CCC',
        )
        self.actions_menu.add_command(label = 'Search', command = lambda : self.render_text_page())
        self.actions_menu.add_command(label = 'History', command = lambda : self.show_history())
        self.actions_menu.add_command(label = 'Configuration', command = lambda : self.show_configuration_center())
        self.actions_menu.add_command(label = 'Exit', command = lambda : self.exit_ui())

        self.help_menu = Menu(
            self.bar_menu,
            tearoff = 0,
            bg = '#666',
            fg = '#CCC',
            activebackground = '#777',
            activeforeground = '#CCC',
        )
        self.help_menu.add_command(label = 'About', command = lambda : msn.show_about())
        self.help_menu.add_command(label = 'Contact', command = lambda : msn.show_contact())

        self.bar_menu.add_cascade(label = 'Actions', menu = self.actions_menu)
        self.bar_menu.add_cascade(label = 'Help', menu = self.help_menu)

        # seting the menu of the window
        self.wind.config(menu = self.bar_menu)


    def create_ui(self) -> None:
        """
        Create the ui in the window
        passed for parameter.
        """

        # creating frame for set the search bar and the search button
        self.frame = Frame(self.wind, bg = self.__COLOR_UI)
        self.frame.grid(column = 0, row = 0)

        self.search_bar = Entry(
            self.frame,
            width = 85,
            selectforeground='#66728C',
            takefocus=True,
            relief='flat',
        )
        self.search_bar.grid(column = 0, row = 0, padx = 10, pady = 10)

        self.search_button = Button(
            self.frame,
            text = 'Search',
            bg = '#353535',
            activebackground = '#454545',
            fg = '#CCC',
            activeforeground = '#CCC',
            cursor = 'hand2',
            relief = 'solid',
        )

        self.search_button['command'] = lambda : self.render_text_page()
        self.search_button.grid(column = 1, row = 0, padx = 10, pady = 10)


        # Scrollbar for the html view no implemented
        # self.scrollbar = Scrollbar(self.wind)
        # self.scrollbar.grid(column = 0, row = 2)

    def render_text_page(self) -> None:
        """
        Render the html in the ui.
        """

        # getting data
        url = self.get_content_search_bar()
        datetime_current = ut.get_date_current()
        # saving search in the history
        ut.save_in_history(Search(datetime_current, url))

        html_content = self.make_request(url)

        page = HTMLLabel(
            self.wind,
            html = html_content,
            bg = '#FFF',
            height = 35,
            # yscrollcommand = self.scrollbar,
        )
        page.grid(
            column = 0,
            row = 1,
            padx = 15,
            pady = 20,
            sticky = 'wesn',
        )

    def get_content_search_bar(self) -> str:
        """
        Return the url of the search bar.
        """

        # getting data for return the search
        url_content = str(self.search_bar.get())
        url_formated = ut.get_formated_url(url_content)
        url_content_list = url_content.split(':')

        if self.SEARCH_ENGINE == 'Google':
            # validating if the word http is is the content for not search in
            # search engine
            if url_content_list[0] == 'http' or url_content_list[0] == 'https':
                url = url_content
            else:
                url = 'https://wwww.google.com/search?q=' + url_formated

        elif self.SEARCH_ENGINE == 'Duck Duck Go':
            if url_content_list[0] == 'http' or url_content_list[0] == 'https':
                url = url_content
            else:
                url = 'https://www.duckduckgo.com/?q=' + url_formated

        return url

    def make_request(self, url:str) -> str:
        """
        Make get request and return the
        html page responsed.
        """

        # execptions handler in case of error
        if url == 'https://wwww.google.com/search?q=' or url == 'https://www.duckduckgo.com/?q=':
            html_content = err.SEARCH_SOME_ERROR
        else:
            try:
                response = get(url)
                html_content = ut.get_valid_html(response, url)

            except InvalidSchema:
                html_content = err.CONECTION_REFUSED
            except MissingSchema:
                html_content = err.URL_INVALID
            except InvalidURL:
                html_content = err.URL_INVALID
            # except ConnectionError:
                # html_content = err.CONNECTION_ERROR
            except ConnectTimeout:
                html_content = err.CONNECTION_TIMEOUT

        # finallly return html content but a valid
        return html_content


    def show_history(self):
        """
        Show a new window for see
        the navegation history.
        """

        # creating window, table and actions buttons
        history_wind = Toplevel(self.wind)
        history_wind.title('History')
        self.wind.tk.call('wm', 'iconphoto', history_wind._w, PhotoImage(file = self.LOGO_PATH))
        # no resizable of top and bottom
        history_wind.resizable(False, False)
        history_wind.config(bg = self.__COLOR_UI)

        self.table = ttk.Treeview(
            history_wind,
            height = 10,
            columns = 2,
        )
        self.table.heading('#0', text = 'Date & Time', anchor = CENTER)
        self.table.heading('#1', text = 'Url Content', anchor = CENTER)

        self.table.grid(column = 0, row = 0, columnspan = 2)

        clear_history_button = Button(
            history_wind,
            text = 'Clean History',
            bg = '#353535',
            activebackground = '#454545',
            fg = '#CCC',
            activeforeground = '#CCC',
            cursor = 'hand2',
            relief = 'solid',
        )
        clear_history_button['command'] = lambda : self.clear_history_ui()
        clear_history_button.grid(column = 0, row = 1, padx = 5, pady = 5)

        copy_history_button = Button(
            history_wind,
            text = 'Copy Selected',
            bg = '#353535',
            activebackground = '#454545',
            fg = '#CCC',
            activeforeground = '#CCC',
            cursor = 'hand2',
            relief = 'solid',
        )
        copy_history_button['command'] = lambda : ut.copy_to_clipboard(self.table.item(self.table.selection())['values'][0])
        copy_history_button.grid(column = 1, row = 1, padx = 5, pady = 5)

        exit_button = Button(
            history_wind,
            text = 'Exit',
            bg = '#353535',
            activebackground = '#454545',
            fg = '#CCC',
            activeforeground = '#CCC',
            cursor = 'hand2',
            relief = 'solid',
            width = 30,
        )
        exit_button['command'] = lambda : history_wind.destroy()
        exit_button.grid(column = 0, row = 2, padx = 5, pady = 10, columnspan = 2)

        # filling the history table
        self.fill_history_table()

    def clear_history_ui(self):
        """
        Clear the history executing
        the cleaning the history file
        and filling the history table again.
        """

        ut.clear_history()
        self.fill_history_table()

    def clear_history_table(self):
        """
        Clear elements of the table.
        """

        # deleting each element
        for element in self.table.get_children():
            self.table.delete(element)

    def fill_history_table(self):
        HISTORY_OBJECT = ut.get_history()

        # validating if the history is empty
        if 'HISTORY' in HISTORY_OBJECT:
            if HISTORY_OBJECT['HISTORY'] != []:

                # cleaning the table
                self.clear_history_table()

                # getting the list of the history insert using for loop
                history_list = ut.get_history()['HISTORY']

                # inserting the history data
                for content in history_list:
                    date = content['dateTime']
                    url_content = content['url']

                    self.table.insert('', 0, text = date, value = url_content)
            else:
                self.clear_history_table()
                self.table.insert('', 0, text = 'Emtpy', value = 'Emtpy')
        else:
            self.clear_history_table()
            self.table.insert('', 0, text = 'Emtpy', value = 'Emtpy')

    def show_configuration_center(self):
        """
        Show a window with configuration
        center.
        """

        # creating window
        self.config_wind = Toplevel(self.wind)
        self.config_wind.title('Configuration Center')
        self.config_wind.tk.call('wm', 'iconphoto', self.config_wind._w, PhotoImage(file = self.LOGO_PATH))

        self.config_wind.resizable(False, False)
        self.config_wind.config(bg = self.__COLOR_UI)

        initial_message = Label(
            self.config_wind,
            text = "Welcome to the configuration center",
            bg = self.__COLOR_UI,
            fg = '#CCC',
            justify = 'center',
        )
        initial_message.grid(column = 0, row = 0, padx = 10, pady = 10, columnspan = 2)

        change_color_button = Button(
            self.config_wind,
            text = 'Change Color Interface',
            bg = '#252525',
            activebackground = '#353535',
            fg = '#CCC',
            activeforeground = '#CCC',
            cursor = 'hand2',
            relief = 'solid',
        )
        change_color_button['command'] = lambda : self.change_color_handler()
        change_color_button.grid(column = 0, row = 1, padx = 10, pady = 15)

        change_search_engine_button = Button(
            self.config_wind,
            text = 'Change Search Engine',
            bg = '#252525',
            activebackground = '#353535',
            fg = '#CCC',
            activeforeground = '#CCC',
            cursor = 'hand2',
            relief = 'solid',
        )
        change_search_engine_button['command'] = lambda : self.change_search_engine_handler()
        change_search_engine_button.grid(column = 1, row = 1, padx = 10, pady = 15)

        exit_button = Button(
            self.config_wind,
            text = 'Exit',
            bg = '#252525',
            activebackground = '#353535',
            fg = '#CCC',
            activeforeground = '#CCC',
            cursor = 'hand2',
            relief = 'solid',
            width = 25,
        )
        exit_button['command'] = lambda : self.config_wind.destroy()
        exit_button.grid(column = 0, row = 2, padx = 10, pady = 10, columnspan = 2)

    def change_color_handler(self) -> None:
        """
        Manage the color change,
        assing the color in the
        window lauch.
        """

        # getting and assing the new color ui
        color_choosed = msn.show_color_chooser()
        ut.change_value_in_config('COLOR', color_choosed)

    def change_search_engine_handler(self):
        # creating the new window for choose
        choose_search_engine_wind = Toplevel(self.config_wind)
        choose_search_engine_wind.title('Select Search Engine')

        choose_search_engine_wind.tk.call('wm', 'iconphoto', choose_search_engine_wind._w, PhotoImage(file = self.LOGO_PATH))
        choose_search_engine_wind.resizable(False, False)

        choose_search_engine_wind.config(bg = self.__COLOR_UI)


        search_engine_table = ttk.Treeview(
            choose_search_engine_wind,
            height = 10,
            columns = 2,
        )
        search_engine_table.heading('#0', text = 'Search Engine', anchor = CENTER)

        search_engine_table.insert('', 0, text = 'Google')
        search_engine_table.insert('', 0, text = 'Duck Duck Go')

        search_engine_table.grid(column = 0, row = 0, columnspan = 2)

        select_search_engine_button = Button(
            choose_search_engine_wind,
            text = 'Select',
            bg = '#252525',
            activebackground = '#353535',
            fg = '#CCC',
            activeforeground = '#CCC',
            cursor = 'hand2',
            relief = 'solid',
            width = 10,
        )
        select_search_engine_button['command'] = lambda : ut.change_value_in_config('SEARCH_ENGINE', search_engine_table.item(search_engine_table.selection())['text'])
        select_search_engine_button.grid(column = 0, row = 1, padx = 5, pady = 10)

        exit_button = Button(
            choose_search_engine_wind,
            text = 'Exit',
            bg = '#252525',
            activebackground = '#353535',
            fg = '#CCC',
            activeforeground = '#CCC',
            cursor = 'hand2',
            relief = 'solid',
            width = 10,
        )
        exit_button['command'] = lambda : choose_search_engine_wind.destroy()
        exit_button.grid(column = 1, row = 1, padx = 5, pady = 10)

    def exit_ui(self) -> None:
        """
        Exit handler for the ui, asking if the user
        want exit
        """

        response = msn.ask_if_exit()

        if response == 'yes':
            self.wind.destroy()
