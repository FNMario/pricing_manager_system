from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from screens.widgets.optionpopup import OptionPopup

from interface import get_product_prices, get_products_for_sale, number_category

import logging
import time

Builder.load_file('screens/buy_screen.kv')


class Buy(Widget):
    searching_text_input = ObjectProperty()

    # Form

    def btn_search_product_on_press(self):
        self.searching_text_input = self.ids.txt_product
        product = self.ids.txt_product.text
        self.ids.tbl_products.items = get_products_for_sale(product=product)

    def btn_search_local_code_on_press(self):
        self.searching_text_input = self.ids.txt_local_code
        code = self.ids.txt_local_code.text
        self.ids.tbl_products.items = get_products_for_sale(local_code=code)

    # Buttons

    def btn_add_price_on_press(self, fraction: int = None):

        def select_fraction():

            def popup_exit(self):
                if self.selected_option:
                    enter_quantity(self.selected_option)

            popup = OptionPopup(
                exit_focus=self.ids.txt_product,
                options=[
                    self.ids.lbl_quantity_1.text,
                    self.ids.lbl_quantity_2.text,
                    self.ids.lbl_quantity_3.text,
                ]
            )
            popup.bind(on_dismiss=popup_exit)
            popup.open()

        def enter_quantity(fraction):
            # print(f'fraction selected: {fraction}')
            input_quantity = [
                self.ids.sm_add_fraction_1,
                self.ids.sm_add_fraction_2,
                self.ids.sm_add_fraction_3
            ]
            input_quantity[fraction].current = "txt"

            def popup_exit(self):
                # if self.quantity > 0
                # add_item_to_budge(self.quantity)
                print('add_item')

            # popup = OptionPopup()
            # popup.bind(on_dismiss=popup_exit)
            # popup.open()

        if fraction is None:
            select_fraction()
        else:
            enter_quantity(fraction)

    def add_item_to_budge(self, fraction_string, quantity):
        if float(quantity) < 1 or fraction_string == '-':
            logging.info("Item not added")
            return

        total = float(quantity)

        for s in fraction_string.split(' '):
            try:
                total = float(s) * float(quantity)
            except:
                pass
        logging.info(
            f"Item added: {total} {fraction_string.split(' ')[-1]}")

    def btn_clean_on_press(self):
        self.clean_forms(self.ids.form_layout)
        self.clean_labels()
        self.clean_table()

    def clean_forms(self, parent):
        for child in parent.children:
            if child.children:
                self.clean_forms(child)
            else:
                if isinstance(child, TextInput):
                    child.text = ""

    def clean_labels(self):
        self.ids.lbl_date.text = "00/00/0000"
        self.ids.lbl_price_1.text = "0.00"
        self.ids.lbl_price_2.text = "0.00"
        self.ids.lbl_price_3.text = "0.00"
        self.ids.lbl_quantity_1.text = "-"
        self.ids.lbl_quantity_2.text = "-"
        self.ids.lbl_quantity_3.text = "-"

    def clean_table(self):
        self.ids.tbl_products.items = []
        self.ids.tbl_products.update_table()

    # Table

    def on_selected_row(self):
        table = self.ids.tbl_products
        if table.items:
            product = table.items[table.selected_row]
            self.ids.txt_product.text = product[1]
            self.ids.txt_local_code.text = product[0]
            self.ids.lbl_quantity.text = product[2]
            prices, quantities, date = get_product_prices(
                product_code=product[0])
            category = number_category(self.ids.lbl_category.text)
            self.ids.lbl_quantity_1.text = quantities[0]
            self.ids.lbl_quantity_2.text = quantities[1]
            self.ids.lbl_quantity_3.text = quantities[2]
            self.ids.lbl_price_1.text = format_numeric_economy(
                prices[0][category])
            self.ids.lbl_price_2.text = format_numeric_economy(
                prices[1][category])
            self.ids.lbl_price_3.text = format_numeric_economy(
                prices[2][category])
            self.ids.lbl_date.text = date
            self.searching_text_input.select_all()


def format_numeric_economy(price: float):
    return f'{price:,.2f}'.replace(',', chr(0x2009)).replace('.', ',')
