from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
import logging

Builder.load_file('screens/buy_screen.kv')

class Buy(Widget):

    def search_product(self):
        return []

    def search_local_code(self):
        return []

    def clean_forms(self, parent):
        for child in parent.children:
            if child.children:
                self.clean_forms(child)
            else:
                if isinstance(child, TextInput): 
                    child.text = ""

    def clean_all(self):
        self.clean_forms(self.ids.form_layout)
        self.ids.lbl_date.text = "00/00/0000"
        self.ids.tbl_products.items = []
        self.ids.tbl_products.update_table()