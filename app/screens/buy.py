from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from screens.widgets.optionpopup import OptionPopup

from interface import format_numeric_economy, get_product_prices, get_products_for_sale, number_category

import logging

Builder.load_file('screens/buy_screen.kv')


class Buy(Widget):
    searching_text_input = ObjectProperty()
    prices = [0, 0, 0]
    fractions = ['-', '-', '-']
    category = 0

    # Form

    def btn_search_product_on_press(self):
        self.searching_text_input = self.ids.txt_product
        product = self.ids.txt_product.text
        self.ids.tbl_products.items = get_products_for_sale(product=product)

    def btn_search_local_code_on_press(self):
        self.searching_text_input = self.ids.txt_local_code
        code = self.ids.txt_local_code.text
        self.ids.tbl_products.items = get_products_for_sale(local_code=code)

    def on_category_change(self, instance):
        self.category = instance.selected_option
        self.on_selected_row()

    # Buttons

    def btn_add_price_on_press(self, fraction: int = None):

        def select_fraction():

            def popup_exit(self):
                if self.selected_option in [0, 1, 2]:
                    enter_quantity(self.selected_option)

            popup = OptionPopup(
                exit_focus=self.ids.txt_product,
                options=[_ for _ in self.fractions if _ != '-']
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

        if fraction is None:
            select_fraction()
        else:
            enter_quantity(fraction)

    def add_item_to_budge(self, fraction, quantity):
        fraction_string = self.fractions[fraction]
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
            f"Item added: {total} {fraction_string.split(' ')[-1]} for ${float(self.prices[fraction][self.category]) * float(quantity)}")

    def btn_clean_on_press(self):
        self.clean_variables()
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

    def clean_variables(self):
        self.prices = [0, 0, 0]
        self.fractions = ['-', '-', '-']

    # Table

    def on_selected_row(self):
        table = self.ids.tbl_products
        if table.items:
            product = table.items[table.selected_row]
            self.ids.txt_product.text = product[1]
            self.ids.txt_local_code.text = product[0]
            self.ids.lbl_quantity.text = product[2]
            self.prices, self.fractions, date = get_product_prices(
                product_code=product[0])
            self.ids.lbl_quantity_1.text = self.fractions[0]
            self.ids.lbl_quantity_2.text = self.fractions[1]
            self.ids.lbl_quantity_3.text = self.fractions[2]
            self.ids.lbl_price_1.text = format_numeric_economy(
                self.prices[0][self.category])
            self.ids.lbl_price_2.text = format_numeric_economy(
                self.prices[1][self.category])
            self.ids.lbl_price_3.text = format_numeric_economy(
                self.prices[2][self.category])
            self.ids.lbl_date.text = date
            self.searching_text_input.focus = True
            self.searching_text_input.select_all()
