from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from screens.widgets.textfield import TextField
from kivy.lang import Builder
from interface import get_dollars, get_fractions, get_ivas, get_sections, get_suppliers, save_dollars, save_fraction, save_ivas, save_section, save_supplier

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

    def get_dict_from_form(self, form):
        data = dict()
        for field in form.children:
            if isinstance(field, TextField):
                for widget in field.children:
                    if isinstance(widget, TextInput):
                        key = widget.hint_text.lower().replace(' ', '_')
                        value = widget.text
                        data[key] = value
        return data

    def btn_save_fraction(self, form):
        data = self.get_dict_from_form(form)
        try:
            assert save_fraction(data)
            self.ids.tbl_fractions.items = self.get_fractions_items()
            self.clear_form(form)
            self.parent.get_screen(
                "manage").ids.optxt_unit.options = self.parent.get_screen("manage").get_units()
        except AssertionError as e:
            logging.error(f"Error saving fraction: {e}")

    def btn_add_fraction(self, form):
        data = self.get_dict_from_form(form)
        data.pop('id')
        try:
            assert save_fraction(data)
            self.ids.tbl_fractions.items = self.get_fractions_items()
            self.clear_form(form)
            self.parent.get_screen(
                "manage").ids.optxt_unit.options = self.parent.get_screen("manage").get_units()
        except AssertionError as e:
            logging.error(f"Error adding fraction: {e}")

    def btn_save_supplier(self, form):
        data = self.get_dict_from_form(form)
        try:
            assert save_supplier(data)
            self.ids.tbl_suppliers.items = self.get_suppliers_items()
            self.clear_form(form)
            self.parent.get_screen("manage").ids.optxt_supplier.options = self.parent.get_screen(
                "manage").get_suppliers()
        except AssertionError as e:
            logging.error(f"Error saving supplier: {e}")

    def btn_add_supplier(self, form):
        data = self.get_dict_from_form(form)
        data.pop('id')
        try:
            assert save_supplier(data)
            self.ids.tbl_suppliers.items = self.get_suppliers_items()
            self.clear_form(form)
            self.parent.get_screen("manage").ids.optxt_supplier.options = self.parent.get_screen(
                "manage").get_suppliers()
        except AssertionError as e:
            logging.error(f"Error adding supplier: {e}")

    def btn_save_section(self, form):
        data = self.get_dict_from_form(form)
        try:
            assert save_section(data)
            self.ids.tbl_sections.items = self.get_sections_items()
            self.clear_form(form)
            self.parent.get_screen("manage").ids.optxt_section.options = self.parent.get_screen(
                "manage").get_sections()
        except AssertionError as e:
            logging.error(f"Error saving section: {e}")

    def btn_add_section(self, form):
        data = self.get_dict_from_form(form)
        data.pop('id')
        try:
            assert save_section(data)
            self.ids.tbl_sections.items = self.get_sections_items()
            self.clear_form(form)
            self.parent.get_screen("manage").ids.optxt_section.options = self.parent.get_screen(
                "manage").get_sections()
        except AssertionError as e:
            logging.error(f"Error adding section: {e}")

    def btn_save_iva(self, row: int, value: float):
        try:
            assert save_ivas(row=row, iva=value)
            self.ids.tbl_iva.items = self.get_iva_items()
            self.clear_form(self.ids.lyt_form_iva)
        except AssertionError as e:
            logging.error(f"Error saving iva: {e}")

    def btn_add_iva(self, value: float):
        try:
            assert save_ivas(iva=value)
            self.ids.tbl_iva.items = self.get_iva_items()
            self.clear_form(self.ids.lyt_form_iva)
        except AssertionError as e:
            logging.error(f"Error saving iva: {e}")

    def btn_save_dollar(self, row: int, value: float):
        try:
            assert save_dollars(row=row, dollar=value)
            self.ids.tbl_dollar.items = self.get_dollar_items()
            self.clear_form(self.ids.lyt_form_dollar)
        except AssertionError as e:
            logging.error(f"Error saving dollar: {e}")

    def btn_add_dollar(self, value: float):
        try:
            assert save_dollars(dollar=value)
            self.ids.tbl_dollar.items = self.get_dollar_items()
            self.clear_form(self.ids.lyt_form_dollar)
        except AssertionError as e:
            logging.error(f"Error saving dollar: {e}")

    def clear_form(self, form):
        for field in form.children:
            if isinstance(field, TextField):
                for widget in field.children:
                    if isinstance(widget, TextInput):
                        widget.text = ""
