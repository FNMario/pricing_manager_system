from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import BooleanProperty, ListProperty, ObjectProperty
from kivy.lang import Builder
from KivyCalendar import DatePicker

from interface import calculate_prices, delete_product, format_numeric_economy, get_date, get_dollar_price, get_dollars, get_fractions, get_ivas, get_last_code, get_products, get_sections, get_suppliers, save_product

import logging

Builder.load_file('screens/manage_prices_screen.kv')


class ManagePrices(Screen):
    products = ListProperty()
    searching_text_input = ObjectProperty()

    def __init__(self, **kw):
        super(ManagePrices, self).__init__(**kw)
        self.bind(products=self.update_table_items)

    # Form

    def btn_search_product_on_press(self):
        self.searching_text_input = self.ids.txt_product
        self.products = get_products(product_id=self.ids.txt_product.text)

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
        self.searching_text_input = self.ids.txt_local_code
        self.products = get_products(local_code=self.ids.txt_local_code.text)

    def get_suppliers(self):
        suppliers = [_[1] for _ in get_suppliers()]
        return suppliers

    def btn_search_suppliers_code_on_press(self):
        self.searching_text_input = self.ids.txt_supplier_code
        self.products = get_products(supplier_code=self.ids.txt_product.text)

    def get_units(self):
        fractions = get_fractions()
        units = [_[1] for _ in fractions]
        return units

    def get_sections(self):
        sections = [_[1] for _ in get_sections()]
        return sections

    def update_prices(self):
        cost = self.ids.txt_cost.text
        surcharge = self.ids.txt_surcharge.text
        quantity = self.ids.txt_quantity.text
        unit = self.ids.optxt_unit.text

        if not cost or not surcharge or not quantity or not unit:
            self.ids.prices_tab.clean_prices()
            return

        cost = float(cost)
        surcharge = float(surcharge) / 100
        quantity = float(quantity)

        prices, fractions, str_unit = calculate_prices(
            quantity=quantity, unit=unit, cost=cost, surcharge=surcharge)
        self.ids.prices_tab.prices = prices
        self.ids.prices_tab.fractions = [
            f'{fr} {str_unit}' for fr in fractions]

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

    def btn_surcharges_plus_on_press(self):
        surcharge = self.ids.txt_surcharge.text
        if surcharge:
            surcharge = str(int(surcharge) + 1)
            self.ids.txt_surcharge.text = surcharge
        else:
            self.ids.txt_surcharge.text = "1"

    def btn_surcharges_minus_on_press(self):
        surcharge = self.ids.txt_surcharge.text
        if surcharge:
            surcharge = str(int(surcharge) - 1)
            self.ids.txt_surcharge.text = surcharge

    def show_calendar(self):
        datePicker = CustomDatePicker()
        datePicker.show_popup(1, 1)

    def btn_refresh_date_on_press(self):
        self.ids.txt_date.text = get_date()

    def current_data(self) -> dict:
        data = {
            'product': self.ids.txt_product.text,
            'local_code': self.ids.txt_local_code.text,
            'supplier': self.ids.optxt_supplier.text,
            'supplier_code': self.ids.txt_supplier_code.text,
            'quantity': float(self.ids.txt_quantity.text) if self.ids.txt_quantity.text else 0,
            'unit': self.ids.optxt_unit.text,
            'cost': float(self.ids.txt_cost.text) if self.ids.txt_cost.text else 0,
            'surcharge': int(self.ids.txt_surcharge.text)/100 if self.ids.txt_surcharge.text else 0,
            'section': self.ids.optxt_section.text,
            'date': self.ids.txt_date.text,
            'iva': float(self.ids.lbl_iva.value) if self.ids.lbl_iva.value else 0,
            'dollar': float(self.ids.lbl_dollar.value) if self.ids.lbl_dollar.value else 0,
        }
        return data

    def get_fields(self) -> dict:
        fields = {
            'product': self.ids.txt_product,
            'local_code': self.ids.txt_local_code,
            'supplier': self.ids.optxt_supplier,
            'supplier_code': self.ids.txt_supplier_code,
            'quantity': self.ids.txt_quantity,
            'unit': self.ids.optxt_unit,
            'cost': self.ids.txt_cost,
            'surcharge': self.ids.txt_surcharge,
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
                           'unit', 'cost', 'section', 'date']
        for field, value in data.items():
            if field in required_fields and not value:
                logging.error(f"{field} field can not be null")
                self.get_fields()[field].focus = True
                return
        try:
            save_product(data)
            self.searching_text_input.focus = True
            self.searching_text_input.select_all()
        except Exception as e:
            logging.error(e)

    def btn_add_on_press(self):
        self.btn_save_on_press()

    def btn_delete_on_press(self):
        data = self.current_data()
        logging.info(f"Deleting product {data}")
        if not data['local_code']:
            logging.error("Local code cannot be empty")
            self.get_fields()['local_code'].focus = True
            return

        try:
            delete_product(data)
            selected_row = self.ids.tbl_products.selected_row
            self.products.pop(selected_row)
            self.ids.tbl_products.selected_row = selected_row
        except Exception as e:
            logging.error(e)

    def btn_replace_on_press(self):
        data = self.current_data()

        required_fields = ['product', 'local_code', 'supplier', 'quantity',
                           'unit', 'cost', 'surcharge', 'section', 'date']
        for field, value in data.items():
            if field in required_fields and not value:
                logging.error('There are empty fields')
                self.get_fields()[field].focus = True
                return
        try:
            delete_product(data, all_costs=True)
            save_product(data)
            self.btn_clean_on_press()
        except Exception as e:
            logging.error(e)

    def btn_compare_on_press(self):
        pass

    def btn_clean_on_press(self):
        self.clean_form()
        self.products = []

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

    def update_table_items(self, instance, items):
        self.ids.tbl_products.items = [(
            p[1],
            p[0],
            f"{p[4]} {p[5]}",
            p[2],
            str(p[3]).replace('None', '-'),
            format_numeric_economy(p[6]*p[7]),
            p[9]
        ) for p in items]

    def on_selected_row(self):
        table = self.ids.tbl_products
        if table.items:
            item = self.products[table.selected_row]
            item = list(map(lambda val: '' if val is None else str(val), item))
            self.ids.txt_product.text = item[0]
            self.ids.txt_local_code.text = item[1]
            self.ids.optxt_supplier.text = item[2]
            self.ids.txt_supplier_code.text = item[3]
            self.ids.txt_quantity.text = item[4]
            self.ids.optxt_unit.text = item[5]
            self.ids.txt_cost.text = item[6]
            self.ids.txt_surcharge.text = str(round(float(item[7]) * 100))
            self.ids.optxt_section.text = item[8]
            self.ids.txt_date.text = item[9]

            self.searching_text_input.focus = True
            self.searching_text_input.select_all()


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
