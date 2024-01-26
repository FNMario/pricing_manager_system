from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from interface import get_clients

import logging


Builder.load_file('screens/clients_screen.kv')


class Clients(Screen):

    def get_clients_items(self):
        clients = get_clients()

        return clients

    def on_selected_row(self, items):
        table = self.ids.tbl_clients
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
        pass

    def btn_save_client_on_press(self):
        pass

    def clear_form_on_press(self):
        pass
