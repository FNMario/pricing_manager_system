from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.lang import Builder

from interface import find_per_local_code, find_per_product_name, find_per_suppliers_code, get_date, get_dollar_price, get_last_code

import logging

Builder.load_file('screens/manage_prices_screen.kv')


class ManagePrices(Widget):

    # Form

    def btn_search_product_on_press(self):
        self.ids.tbl_products.items = find_per_product_name(
            self.ids.txt_product.text)

    def btn_next_code_on_press(self):
        local_code = self.ids.txt_local_code.text
        if len(local_code) >= 4:
            base = local_code[:4]
            number = local_code[4:]
            try:
                number = str(int(number) + 1).zfill(3)
            except ValueError:
                number = '001'
            local_code = base + number
            self.ids.txt_local_code.text = local_code

    def btn_new_code_on_press(self):
        local_code = self.ids.txt_local_code.text
        if len(local_code) >= 4:
            base = local_code[:4]
            number = str(int(get_last_code(base)[4:]) + 1)
            local_code = base + number
            self.ids.txt_local_code.text = local_code

    def btn_search_local_code_on_press(self):
        self.ids.tbl_products.items = find_per_local_code(
            self.ids.txt_local_code.text)

    def btn_search_suppliers_code_on_press(self):
        self.ids.tbl_products.items = find_per_suppliers_code(
            self.ids.txt_product.text)

    def update_prices(self):
        cost = self.ids.txt_cost.text
        earning = self.ids.txt_earning.text
        if cost and earning:
            cost = float(cost)
            earning = float(earning) / 100
            price = cost * earning
            print(price)

    def calculate_cost(self, include: list[str] = ["iva", "dollar"]):
        cost = self.ids.txt_cost.text
        if cost:
            cost = float(cost)
            if "iva" in include:
                cost = self.add_iva(cost)
            if "dollar" in include:
                cost = self.add_dollar(cost)
            self.ids.txt_cost.text = str(round(cost, 6))

    def add_iva(self, cost):
        iva_active = self.ids.chk_iva.active
        iva = 1 + self.ids.lbl_iva.value / 100
        return cost * iva if iva_active else cost

    def add_dollar(self, cost):
        dollar_active = self.ids.chk_dollar.active
        dollar = self.ids.lbl_dollar.value
        return cost * dollar if dollar_active else cost

    def change_iva(self):
        pass

    def get_dollar_price(self):
        return get_dollar_price()

    def change_dollar(self):
        pass

    def btn_earnings_plus_on_press(self):
        earning = self.ids.txt_earning.text
        if earning:
            earning = str(int(earning) + 1)
            self.ids.txt_earning.text = earning

    def btn_earnings_minus_on_press(self):
        earning = self.ids.txt_earning.text
        if earning:
            earning = str(int(earning) - 1)
            self.ids.txt_earning.text = earning

    def btn_refresh_date_on_press(self):
        self.ids.txt_date.text = get_date()

    # Buttons

    def btn_save_on_press(self):
        pass

    def btn_add_on_press(self):
        pass

    def btn_delete_on_press(self):
        pass

    def btn_replace_on_press(self):
        pass

    def btn_compare_on_press(self):
        pass

    def btn_clean_on_press(self):
        self.clean_forms(self.ids.form_layout)
        self.ids.tbl_products.items = []
        self.ids.prices_tab.clean_prices()

    def clean_forms(self, parent):
        for child in parent.children:
            if child.children:
                self.clean_forms(child)
            else:
                if isinstance(child, TextInput):
                    child.text = ""


class PriceManagerApp(App):
    def build(self):
        Window.clearcolor = (.13, .14, .19, 1)
        return ManagePrices()


class PricesTab(BoxLayout):

    no_data = [
        ["0.00", "0.00", "0.00", "-"],
        ["0.00", "0.00", "0.00", "-"],
        ["0.00", "0.00", "0.00", "-"]
    ]

    def __init__(self, **kwargs):
        super(PricesTab, self).__init__(**kwargs)
        self.data = self.no_data

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.height == 150:
                self.blank()
                self.height = 40
                self.pos_hint = {'center_y': 0.05}
            else:
                self.load_data(self.data)
                self.height = 150
                self.pos_hint = {'center_y': 0.5}

    def clean_prices(self):
        self.load_data(
            self.no_data
        )

    def blank(self):
        self.load_data(
            [
                ["", "", "", ""],
                ["", "", "", ""],
                ["", "", "", ""]
            ],
            save_data=False
        )

    def load_data(self, data: list[list[str]], save_data=True):
        if len(data):
            assert len(data[0]) == 4
            self.ids.lbl_price_V_1.text = data[0][0]
            self.ids.lbl_price_D_1.text = data[0][1]
            self.ids.lbl_price_M_1.text = data[0][2]
            self.ids.lbl_quantity_1.text = data[0][3]
        if len(data) >= 1:
            assert len(data[1]) == 4
            self.ids.lbl_price_V_2.text = data[1][0]
            self.ids.lbl_price_D_2.text = data[1][1]
            self.ids.lbl_price_M_2.text = data[1][2]
            self.ids.lbl_quantity_2.text = data[1][3]
        if len(data) >= 2:
            assert len(data[2]) == 4
            self.ids.lbl_price_V_3.text = data[2][0]
            self.ids.lbl_price_D_3.text = data[2][1]
            self.ids.lbl_price_M_3.text = data[2][2]
            self.ids.lbl_quantity_3.text = data[2][3]
        if save_data:
            self.data = data
