from kivy.properties import BooleanProperty, ListProperty, ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from interface import format_numeric_economy, get_dollar_price, get_products, get_sections, get_suppliers
from KivyCalendar import DatePicker

import logging


Builder.load_file('screens/group_raise_screen.kv')


class GroupRaise(Screen):
    products = ListProperty()
    searching_text_input = ObjectProperty()

    def __init__(self, **kwargs):
        super(GroupRaise, self).__init__(**kwargs)
        self.bind(products=self.update_table)

    # Utils

    def all_upper_case(self, instance, max_length: int = None):
        instance.text = instance.text.upper()
        if type(max_length) == int:
            instance.text = instance.text[:max_length]

    # Search form

    def get_suppliers(self):
        suppliers = [_[1] for _ in get_suppliers()]
        return suppliers

    def get_sections(self):
        sections = [_[1] for _ in get_sections()]
        return sections

    def show_calendar(self, instance):
        datePicker = CustomDatePicker(field=instance)
        datePicker.show_popup(1, 1)

    def search(self, instance=None):
        self.searching_text_input = instance
        search_fields = {
            'product': self.ids.txt_product.text,
            'local_code': self.ids.txt_local_code.text,
            'supplier_code': self.ids.txt_supplier_code.text,
            'section': self.ids.optxt_section.text,
            'supplier': self.ids.optxt_supplier.text,
            'from_date': self.ids.txt_from_date.text,
            'to_date': self.ids.txt_to_date.text
        }
        search_fields = {key: value for key,
                         value in search_fields.items() if value}

        products_match = get_products(**search_fields)
        products_match = [
            product for product in products_match if product not in self.products]

        if self.ids.chk_additive.active:
            checked_rows = self.ids.tbl_products.get_checked_rows()
            products = [self.products[row] for row in checked_rows]
            self.products = products + products_match
            if self.searching_text_input:
                self.searching_text_input.text = ""
                self.searching_text_input.focus = True
        else:
            self.products = products_match
            if self.searching_text_input:
                self.searching_text_input.focus = True

    def clear_form(self):
        self.ids.txt_product.text = ''
        self.ids.txt_local_code.text = ''
        self.ids.txt_supplier_code.text = ''
        self.ids.optxt_section.text = ''
        self.ids.optxt_supplier.text = ''
        self.ids.txt_from_date.text = ''
        self.ids.txt_to_date.text = ''
        self.ids.txt_product.focus = True

    # Raise form

    def least_significant_digit_power(self, num_string: str) -> int:
        if '.' in num_string:
            return -len(num_string.partition('.')[2])
        else:
            return 0

    def btn_percentage_plus_on_press(self):
        percentage = self.ids.txt_percentage.text
        if percentage:
            percentage = str(round(
                float(percentage) + 10 ** self.least_significant_digit_power(percentage), 1))
            if int(percentage.split('.')[1]) == 0:
                percentage = percentage.split('.')[0]
            self.ids.txt_percentage.text = percentage
        else:
            self.ids.txt_percentage.text = "1"

    def btn_percentage_minus_on_press(self):
        percentage = self.ids.txt_percentage.text
        if percentage:
            percentage = str(round(
                float(percentage) - 10 ** self.least_significant_digit_power(percentage), 1))
            if int(percentage.split('.')[1]) == 0:
                percentage = percentage.split('.')[0]
            self.ids.txt_percentage.text = percentage

    def get_dollar_price(self):
        return get_dollar_price()

    def update_costs(self):
        self.update_table(None, self.products)

    # Table

    def update_table(self, _, items):
        if self.ids.chk_dollar.active and self.ids.txt_dollar.text:
            dollar_price = float(self.ids.txt_dollar.text)
            self.ids.tbl_products.items = [(
                p[1],
                p[0],
                p[2],
                format_numeric_economy(p[10], True),
                p[9],
                format_numeric_economy(p[6], True),
                format_numeric_economy(float(p[6])/float(p[10])*dollar_price, True)
            ) for p in items]
        elif self.ids.chk_percentage.active and self.ids.txt_percentage.text:
            percentage = 1 + float(self.ids.txt_percentage.text) / 100
            self.ids.tbl_products.items = [(
                p[1],
                p[0],
                p[2],
                format_numeric_economy(p[10], True),
                p[9],
                format_numeric_economy(p[6], True),
                format_numeric_economy(float(p[6]) * percentage, True)
            ) for p in items]

    def on_selected_row(self):
        pass
        # table = self.ids.tbl_products
        # table.switch_checkbox_state(table.selected_row)

    def btn_save_on_press(self):
        self.products.clear()
        self.update_table(None, [])
        self.clear_form()


class CustomDatePicker(DatePicker):
    field = ObjectProperty()

    def update_value(self, inst):
        """ Update textinput value on popup close """

        self.text = "%s/%s/%s" % tuple(self.cal.active_date)
        self.focus = False
        # inst.get_parent_window().children[1].get_screen("home").ids.home_screen_manager.get_screen("manage").ids.txt_date.text
        self.field.text = self.text
