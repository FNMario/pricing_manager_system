from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.core.window import WindowBase
from my_widgets_.datatable import DataTable
from kivy.uix.textinput import TextInput
import logging

class Budget(Widget):

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

class BudgetApp(App):
    def build(self):
        WindowBase.clearcolor = (.13, .14, .19, 1)
        return Budget()


if __name__ == '__main__':
    Config.set('graphics', 'width', '1200')
    Config.set('graphics', 'height', '800')
    Config.write()
    app = BudgetApp()
    app.kv_file = 'budget_screen.kv'
    app.run()
