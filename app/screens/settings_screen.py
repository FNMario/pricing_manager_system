from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from screens.widgets.textfield import TextField
from kivy.lang import Builder
from interface import get_dollars, get_fractions, get_ivas, get_sections, get_suppliers

import logging


Builder.load_file('screens/settings_screen.kv')


class SettingsScreen(Screen):
    id = "settings_screen"
    name = "settings"

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

    def get_fractions_items(self):
        fractions = get_fractions()
        return fractions

    def get_suppliers_items(self):
        suppliers = get_suppliers()
        return suppliers

    def get_sections_items(self):
        sections = get_sections()
        return sections

    def get_iva_items(self):
        ivas = get_ivas()
        ivas = list(map(lambda x: (str(x),), ivas))
        return ivas

    def get_dollar_items(self):
        dollars = get_dollars()
        dollars = list(map(lambda x: (str(x),), dollars))
        return dollars

    def on_selected_row(self, form, item):
        counter = -1
        for field in form.children:
            if isinstance(field, TextField):
                for widget in field.children:
                    if isinstance(widget, TextInput):
                        widget.text = str(item[counter])
                        counter -= 1

    def clear_form(self, form):
        for field in form.children:
            if isinstance(field, TextField):
                for widget in field.children:
                    if isinstance(widget, TextInput):
                        widget.text = ""
