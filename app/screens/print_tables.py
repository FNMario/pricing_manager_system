from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty, ListProperty, ObjectProperty
from kivy.lang import Builder

from interface import add_tables_to_print_name, format_numeric_economy, get_product_prices, get_products_for_sale, get_sections, get_table_to_print_data, get_tables_to_print_names, print_table, save_table_to_print_data, save_tables_to_print_name

import logging


Builder.load_file('screens/print_tables_screen.kv')


class PrintTables(Screen):
    name = "print"
    products = ListProperty()
    searching_text_input = ObjectProperty()
    products_to_print = list()

    def __init__(self, **kwargs):
        super(PrintTables, self).__init__(**kwargs)
        self.bind(products=self.update_table_products)
        self.table_name = dict()

    def all_upper_case(self, instance, max_length: int = None):
        instance.text = instance.text.upper()
        if type(max_length) == int:
            instance.text = instance.text[:max_length]

    # Table name

    def get_sections(self):
        sections = [_[1] for _ in get_sections()]
        return sections

    def clear_tables(self):
        pass

    def btn_search_table_name_on_press(self):
        table = self.ids.tbl_table_name
        table.items = get_tables_to_print_names(
            self.ids.optxt_section.text, self.ids.txt_table_name.text)

    def btn_add_table_name_on_press(self):
        add_tables_to_print_name(
            self.ids.optxt_section.text, self.ids.txt_table_name.text)
        self.btn_search_table_name_on_press()
        self.table_name = {'section': self.ids.optxt_section.text,
                           'name': self.ids.txt_table_name.text}
        self.btn_select_table_on_press()

    def btn_save_table_name_on_press(self):
        table = self.ids.tbl_table_name
        save_tables_to_print_name(
            self.ids.optxt_section.text, table.items[table.selected_row][1], self.ids.txt_table_name.text)
        self.btn_search_table_name_on_press()
        self.table_name = {'section': self.ids.optxt_section.text,
                           'name': self.ids.txt_table_name.text}
        self.btn_select_table_on_press()

    def btn_select_table_on_press(self):
        self.ids.print_tables_screen_manager.current = "print"
        table = self.ids.tbl_table_name
        self.table_name = {'section': self.ids.optxt_section.text,
                           'name': table.items[table.selected_row]}
        rows, headers = get_table_to_print_data(**self.table_name)
        self.products_to_print = [(code, "texto") for code in rows]

        checkboxes_ids = [id for id in self.ids if 'chk_' in id]
        for id in checkboxes_ids:   # deactivate all
            col = self.ids[id]
            if col.active == True:
                col.active = False
                self.update_columns(False, col.text)

        for id in headers:          # activate
            col = self.ids[id]
            if col.active == False:
                col.active = True
                self.update_columns(True, col.text)

    def on_selected_row_table_name(self):
        pass

    # Table products

    def btn_search_product_on_press(self):
        self.searching_text_input = self.ids.txt_product
        product = self.ids.txt_product.text
        self.products = get_products_for_sale(product=product)
        table = self.ids.tbl_products
        table.selected_row = -1

    def btn_search_local_code_on_press(self):
        self.searching_text_input = self.ids.txt_local_code
        code = self.ids.txt_local_code.text
        self.products = get_products_for_sale(local_code=code)
        table = self.ids.tbl_products
        table.selected_row = -1

    def btn_search_supplier_code_on_press(self):
        self.searching_text_input = self.ids.txt_supplier_code
        code = self.ids.txt_supplier_code.text
        self.products = get_products_for_sale(supplier_code=code)
        table = self.ids.tbl_products
        table.selected_row = -1

    def update_table_products(self, instance, items):
        self.ids.tbl_products.items = [(
            p[0],
            p[1],
            p[2],
            p[3],
        ) for p in items]

    def on_selected_row_products(self):
        self.ids.tbl_products.selected_row = -1

    # Table to print

    def btn_add_products_on_press(self):
        table_products = self.ids.tbl_products
        if self.products:
            checked_rows = table_products.get_checked_rows()
            items = [self.products[i] for i in checked_rows]
            self.products_to_print.extend(
                [(item[0], item[1]) for item in items])
            self.update_table_to_print()

    def btn_remove_products_on_press(self):
        table_to_print = self.ids.tbl_table_to_print
        if self.products_to_print:
            checked_rows = table_to_print.get_checked_rows()
            for row in sorted(checked_rows, reverse=True):
                self.products_to_print.pop(row)
            self.update_table_to_print()

    def update_table_to_print(self):
        table_to_print = self.ids.tbl_table_to_print
        if not self.products_to_print:
            table_to_print.items = []

            return
        columns = table_to_print.header
        new_items = list()
        find_prices = False

        if len(columns) > 2:
            columns = columns[2:]
            find_prices = True

        for item in self.products_to_print:
            new_item = list(item)

            if find_prices:
                code = new_item[0]
                prices, quantities, date = get_product_prices(code)

                column_value = {
                    "Venta 1": format_numeric_economy(prices[0][0], True),
                    "Venta 2": format_numeric_economy(prices[1][0], True),
                    "Venta 3": format_numeric_economy(prices[2][0], True),
                    "Descuento 1": format_numeric_economy(prices[0][1], True),
                    "Descuento 2": format_numeric_economy(prices[1][1], True),
                    "Descuento 3": format_numeric_economy(prices[2][1], True),
                    "Mayorista 1": format_numeric_economy(prices[0][2], True),
                    "Mayorista 2": format_numeric_economy(prices[1][2], True),
                    "Mayorista 3": format_numeric_economy(prices[2][2], True),
                    "Fracción 1": quantities[0],
                    "Fracción 2": quantities[1],
                    "Fracción 3": quantities[2],
                    "Date": date,
                }

                values = [column_value[column] for column in columns]
                new_item.extend(values)

            new_items.append(tuple(new_item))

        table_to_print.items = new_items

    def btn_print_table_on_press(self):
        table_to_print = self.ids.tbl_table_to_print
        if self.products_to_print:
            checked_rows = table_to_print.get_checked_rows()
            items_to_print = [table_to_print.items[row]
                              for row in checked_rows]
            save_table_to_print_data(self.products_to_print, table_to_print.header)
            print_table(items_to_print, table_to_print.header)
        else:
            logging.error("No products to print.")

    # def btn_save_description_on_press(self):
    #     table = self.ids.tbl_table_to_print
    #     table.items[table.selected_row][1] = self.ids.txt_description.text

    def on_selected_row_table_to_print(self):
        self.ids.tbl_table_to_print.selected_row = -1
        # table = self.ids.tbl_table_to_print
        # self.ids.txt_description.text = table.items[table.selected_row][1]

    def update_columns(self, is_on: bool, header: str):
        header = header[0].upper() + header[1:].lower()
        table_to_print = self.ids.tbl_table_to_print
        if is_on:
            table_to_print.hint_sizes.append(0.3)
            table_to_print.header.append(header)
        else:
            try:
                table_to_print.header.remove(header)
                table_to_print.hint_sizes.pop()
            except ValueError as e:
                logging.error(f'program_error: print_tables.py: {e}')
        self.update_table_to_print()
