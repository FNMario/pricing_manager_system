from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.lang import Builder
from interface import get_dollars, get_ivas, get_sections, get_suppliers, save_dollars, save_ivas

import logging


Builder.load_file('screens/settings_screen.kv')


class SettingsScreen(Screen):
    id = "settings_screen"
    name = "settings"

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

    def get_iva_items(self):
        ivas = get_ivas()
        ivas = [str(_) for _ in ivas]
        return ivas

    def set_iva_items(self, instance):
        result = save_ivas([float(_) for _ in instance.tmp_items])
        instance.successful_save = result

    def get_dollar_items(self):
        return get_dollars()

    def set_dollar_items(self, instance):
        result = save_dollars([float(_) for _ in instance.tmp_items])
        instance.successful_save = result

    def get_suppliers_items(self):
        suppliers = get_suppliers()
        return suppliers

    def get_sections_items(self):
        sections = get_sections()
        return sections