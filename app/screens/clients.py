from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from interface import get_clients, save_client

import logging


Builder.load_file('screens/clients_screen.kv')


class Clients(Screen):

    def get_clients_items(self):
        clients = get_clients()

        return clients

    def on_selected_row(self, items):
        self.ids.txt_cuit_cuil.text = items[0] if items[0] else ""
        self.ids.txt_name.text = items[1] if items[1] else ""
        self.ids.txt_phone.text = items[3] if items[3] else ""
        self.ids.txt_email.text = items[2] if items[2] else ""
        self.ids.txt_address.text = items[6] if items[6] else ""
        self.ids.txt_city.text = items[5] if items[5] else ""
        self.ids.txt_zip_code.text = str(items[4]) if items[4] else ""

    def max_length(self, instance, max_length: int = None):
        if type(max_length) == int:
            instance.text = instance.text[:max_length]
    
    def btn_search_client_on_press(self):
        search_term = str(self.ids.txt_cuit_cuil.text)
        if not search_term:
            return
        
        table = self.ids.tbl_clients
        items = self.get_clients_items()
        # table.items = items
        cuits = [item[0] for item in items]
        for cuit in cuits:
            if search_term.replace('-', '') in cuit.replace('-', ''):
                table.selected_row = cuits.index(cuit)
                return
        self.clear_form_on_press()
        self.ids.txt_cuit_cuil.text = search_term
        self.ids.txt_cuit_cuil.select_all()

    def btn_save_client_on_press(self):
        client = {
        'cuit_cuil': self.ids.txt_cuit_cuil.text,
        'name': self.ids.txt_name.text,
        'phone': self.ids.txt_phone.text,
        'email': self.ids.txt_email.text,
        'address': self.ids.txt_address.text,
        'city': self.ids.txt_city.text,
        'zip_code': self.ids.txt_zip_code.text,
        }

        try:
            assert save_client(client), 'Error saving client. Please check your data.'
            self.ids.tbl_clients.items = self.get_clients_items()
            self.clear_form_on_press()
        except AssertionError as e:
            logging.error(f'Clients: {e}')

    def clear_form_on_press(self):
        for obj in self.ids.values():
            if isinstance(obj, TextInput):
                obj.text = ""
        self.ids.txt_cuit_cuil.focus = True

