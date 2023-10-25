from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import BooleanProperty, ListProperty
from kivy.lang import Builder
from KivyCalendar import DatePicker

from interface import calculate_prices_from_costs, find_per_local_code, find_per_product_name, find_per_suppliers_code, format_numeric_economy, get_date, get_dollar_price, get_dollars, get_fractions, get_ivas, get_last_code, get_sections, get_suppliers, save_product

import logging

Builder.load_file('screens/manage_prices_screen.kv')


class ManagePrices(Screen):

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

    def get_suppliers(self):
        suppliers = get_suppliers()
        return suppliers

    def btn_search_suppliers_code_on_press(self):
        self.ids.tbl_products.items = find_per_suppliers_code(
            self.ids.txt_product.text)

    def get_units(self):
        fractions = get_fractions()
        units = [line[1] for line in fractions]
        return units

    def get_sections(self):
        sections = get_sections()
        return sections

    def update_prices(self):
        cost = self.ids.txt_cost.text
        earning = self.ids.txt_earning.text
        quantity = self.ids.txt_quantity.text
        unit = self.ids.optxt_unit.text

        if not cost or not earning or not quantity or not unit:
            self.ids.prices_tab.clean_prices()
            return

        cost = float(cost)
        earning = float(earning) / 100
        quantity = float(quantity)

        prices, fractions = calculate_prices_from_costs(
            quantity, unit, cost, earning)
        self.ids.prices_tab.prices = prices
        self.ids.prices_tab.fractions = [f'{fr} {unit}' for fr in fractions]

    def calculate_cost(self):
        cost = self.ids.txt_cost.text
        if cost:
            cost = float(cost)
            iva_active = self.ids.chk_iva.active
            iva = cost * self.ids.lbl_iva.value / 100 * int(iva_active)
            dollar_active = self.ids.chk_dollar.active
            dollar = self.ids.lbl_dollar.value if dollar_active else 1
            cost = (cost + iva) * dollar
            self.ids.txt_cost.text = str(round(cost, 6))

    def change_iva_state(self):
        cost = self.ids.txt_cost.text
        if cost:
            cost = float(cost)
            iva_active = self.ids.chk_iva.active
            iva = 1 + self.ids.lbl_iva.value / 100
            cost = cost * iva if iva_active else cost / iva
            self.ids.txt_cost.text = str(round(cost, 6))

    def change_dollar_state(self):
        cost = self.ids.txt_cost.text
        if cost:
            cost = float(cost)
            dollar_active = self.ids.chk_dollar.active
            dollar = self.ids.lbl_dollar.value
            cost = cost * dollar if dollar_active else cost / dollar
            self.ids.txt_cost.text = str(round(cost, 6))

    def change_iva(self, instance):
        iva_items = get_ivas()
        try:
            index = iva_items.index(instance.value)
            new_index = (index + 1) % len(iva_items)
        except:
            new_index = 0
        instance.value = iva_items[new_index]
        instance.text = f"IVA ({instance.value}%)"

    def get_dollar_price(self):
        return get_dollar_price()

    def change_dollar(self, instance):
        dollar_items = get_dollars()
        try:
            index = dollar_items.index(instance.value)
            new_index = (index + 1) % len(dollar_items)
        except:
            new_index = 0
        instance.value = dollar_items[new_index]
        instance.text = f"IVA ({instance.value}%)"
        instance.text = f"Dollar (${instance.value})"

    def btn_earnings_plus_on_press(self):
        earning = self.ids.txt_earning.text
        if earning:
            earning = str(int(earning) + 1)
            self.ids.txt_earning.text = earning
        else:
            self.ids.txt_earning.text = "1"

    def btn_earnings_minus_on_press(self):
        earning = self.ids.txt_earning.text
        if earning:
            earning = str(int(earning) - 1)
            self.ids.txt_earning.text = earning

    def show_calendar(self):
        datePicker = CustomDatePicker()
        datePicker.show_popup(1, 1)

    def btn_refresh_date_on_press(self):
        self.ids.txt_date.text = get_date()

    def current_data(self) -> list:
        data = {
            'product': self.ids.txt_product.text,
            'local_code': self.ids.txt_local_code.text,
            'supplier': self.ids.optxt_supplier.text,
            'supplier_code': self.ids.txt_supplier_code.text,
            'quantity': self.ids.txt_quantity.text,
            'unit': self.ids.optxt_unit.text,
            'cost': self.ids.txt_cost.text,
            'earning': self.ids.txt_earning.text,
            'section': self.ids.optxt_section.text,
            'date': self.ids.txt_date.text,
            'iva': self.ids.lbl_iva.value,
            'dollar': self.ids.lbl_dollar.value,
        }
        return data

    def get_fields(self) -> list:
        fields = {
            'product': self.ids.txt_product,
            'local_code': self.ids.txt_local_code,
            'supplier': self.ids.optxt_supplier,
            'supplier_code': self.ids.txt_supplier_code,
            'quantity': self.ids.txt_quantity,
            'unit': self.ids.optxt_unit,
            'cost': self.ids.txt_cost,
            'earning': self.ids.txt_earning,
            'section': self.ids.optxt_section,
            'date': self.ids.txt_date,
            'iva': self.ids.lbl_iva,
            'dollar': self.ids.lbl_dollar,
        }
        return fields
    
    def all_upper_case(self, instance):
        instance.text = instance.text.upper()

    # Buttons

    def btn_save_on_press(self):
        data = self.current_data()
        required_fields = ['product', 'local_code', 'supplier', 'quantity',
                           'unit', 'cost', 'earning', 'section', 'date']
        for field, value in data.items():
            if field in required_fields and not value:
                logging.error('There are empty fields')
                self.get_fields()[field].focus = True
                return
        save_product(data)
        self.clean_form()

    def btn_add_on_press(self):
        print(self.doll.value)

    def btn_delete_on_press(self):
        pass

    def btn_replace_on_press(self):
        pass

    def btn_compare_on_press(self):
        pass

    def btn_clean_on_press(self):
        self.clean_form()
        self.ids.tbl_products.items = []

    def clean_form(self):
        def clean_text_input(parent):
            for child in parent.children:
                if child.children:
                    clean_text_input(child)
                else:
                    if isinstance(child, TextInput):
                        child.text = ""

        clean_text_input(self.ids.form_layout)
        self.ids.prices_tab.clean_prices()

    # Table

    def on_selected_row(self):
        table = self.ids.tbl_products
        if table.items:
            selected_row = table.selected_row
            print(table.items[selected_row])

    # TODO: decidir donde y como reducir los elementos recibidos


class PricesTab(BoxLayout):
    hidden = BooleanProperty(False)
    prices = ListProperty([
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ])
    fractions = ListProperty([
        "",
        "",
        ""
    ])

    def format_prices(self, value: float) -> str:
        return format_numeric_economy(value)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.hidden = not self.hidden

    def clean_prices(self):
        self.prices = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.fractions = [
            "",
            "",
            ""
        ]


class CustomDatePicker(DatePicker):

    def update_value(self, inst):
        """ Update textinput value on popup close """

        self.text = "%s/%s/%s" % tuple(self.cal.active_date)
        self.focus = False
        inst.get_parent_window().children[1].get_screen(
            "home").ids.home_screen_manager.get_screen("manage").ids.txt_date.text = self.text
