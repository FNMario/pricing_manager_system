from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
from kivy.lang import Builder
from screens.widgets.messagebox import MessageBox
from screens.widgets.optionpopup import OptionPopup

from interface import format_numeric_economy, get_product_prices, get_products_for_sale

import logging

Builder.load_file('screens/buy_screen.kv')


class Buy(Screen):
    products = ListProperty()
    searching_text_input = ObjectProperty()

    def __init__(self, **kw):
        super(Buy, self).__init__(**kw)
        self.bind(products=self.update_table_items)
        self.prices = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.fractions = ['-', '-', '-']
        self.category = 0
        self.total_budget = 0

    # Form

    def btn_search_product_on_press(self):
        self.searching_text_input = self.ids.txt_product
        product = self.ids.txt_product.text
        self.products = get_products_for_sale(product=product)

    def btn_search_local_code_on_press(self):
        self.searching_text_input = self.ids.txt_local_code
        code = self.ids.txt_local_code.text
        self.products = get_products_for_sale(local_code=code)

    def btn_search_supplier_code_on_press(self):
        self.searching_text_input = self.ids.txt_supplier_code
        code = self.ids.txt_supplier_code.text
        self.products = get_products_for_sale(supplier_code=code)

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
                options=[_ for _ in self.fractions if _ != '-']
            )
            popup.bind(on_dismiss=popup_exit)
            popup.open()

        def enter_quantity(fraction):
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

    def add_item_to_budget(self, fraction, quantity):
        fraction_string = self.fractions[fraction]
        price = self.prices[fraction][self.category]
        quantity = float(quantity)

        if quantity <= 0 or fraction_string == '-' or price <= 0:
            # logging.error("Item not added")
            return

        item = BudgetItem(
            product=self.ids.txt_product.text,
            local_code=self.ids.txt_local_code.text,
            quantity=quantity,
            fraction_level=fraction,
            fraction=fraction_string,
            price=price,
            sales_category=self.ids.optxt_category.text[0]
        )
        item.bind(on_delete_item=self.update_budget_total)
        self.ids.budget_layout.add_widget(item, 2)

        self.update_budget_total()
        self.btn_clean_on_press()

    def btn_clean_on_press(self):
        self.clean_variables()
        self.clean_forms(self.ids.form_layout)
        self.clean_labels()
        self.clean_table()
        if self.searching_text_input:
            self.searching_text_input.focus = True
        else:
            self.ids.txt_product.focus = True

    def clean_forms(self, parent):
        for child in parent.children:
            if child.children:
                self.clean_forms(child)
            else:
                if isinstance(child, TextInput):
                    if child.readonly:
                        continue
                    child.text = ""

    def clean_labels(self):
        self.ids.lbl_quantity.text = "Quantity"
        self.ids.lbl_date.text = "00/00/0000"
        self.ids.lbl_price_1.text = "0.00"
        self.ids.lbl_price_2.text = "0.00"
        self.ids.lbl_price_3.text = "0.00"
        self.ids.lbl_quantity_1.text = "-"
        self.ids.lbl_quantity_2.text = "-"
        self.ids.lbl_quantity_3.text = "-"

    def clean_table(self):
        self.ids.tbl_products.items = []

    def clean_variables(self):
        self.prices = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.fractions = ['-', '-', '-']

    # Table

    def update_table_items(self, instance, items):
        self.ids.tbl_products.items = [(
            p[0],
            p[1],
            p[2],
            p[3],
        ) for p in items]

    def on_selected_row(self):
        table = self.ids.tbl_products
        if table.items:
            product = self.products[table.selected_row]
            self.ids.txt_product.text = product[1]
            self.ids.txt_local_code.text = product[0]
            self.ids.txt_supplier_code.text = str(product[5])
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

    # Budget

    def update_budget_total(self, *args):
        budget_layout = self.ids.budget_layout
        lbl_total_price = self.ids.lbl_total_price

        total = 0

        for child in budget_layout.children:
            if isinstance(child, BudgetItem):
                child.ids.lbl_product_name.text = f"{len(child.parent.children) - child.parent.children.index(child)}. {child.product}"
                total += child.quantity * child.price

        lbl_total_price.text = format_numeric_economy(total, True)

        self.ids.btn_save_budget.disabled = bool(total <= 0)

    def btn_save_budget_on_press(self):
        budgets_screen = self.parent.get_screen('budgets')
        budgets_screen_table = budgets_screen.ids.tbl_budget

        def transfer_budget_to_budgets_screen(perform="yes"):
            if perform == "Cancel":
                return
            children = self.ids.budget_layout.children.copy()
            items = [item.to_tuple()
                     for item in children if isinstance(item, BudgetItem)]
            budgets_screen.budget_items = items
            budgets_screen_table.items = [
                (str(i[1]), i[0], i[4], i[3], str(i[2]), str(i[1]*i[2]))
                for i in items
            ]
            budgets_screen.budget_changed = True
            budgets_screen.is_budget = True
            # go to budgets_screen
            self.get_parent_window(
            ).children[-1].current_screen.ids.btn_budgets.dispatch('on_press')

            self.btn_discard_budget_on_press()

        if self.ids.lbl_budget_title.text == "New budget":
            if not budgets_screen.budget_changed:
                budgets_screen.clear_budget()
                transfer_budget_to_budgets_screen()
            else:
                msg = MessageBox(
                    message=f"""
There is already a budget with changes in 'budgets' screen. \
Are you sure you want to discard those changes \
and continue with this?""",
                    kind='question',
                    buttons=["Continue", "Cancel"],
                    on_close=transfer_budget_to_budgets_screen
                )
        else:
            transfer_budget_to_budgets_screen()

    def btn_discard_budget_on_press(self):
        children = self.ids.budget_layout.children.copy()
        self.ids.lbl_budget_title.text = "New budget"
        for child in children:
            if isinstance(child, BudgetItem):
                child.delete_item()


class BudgetItem(Widget):
    product = StringProperty()
    local_code = StringProperty()
    quantity = NumericProperty()
    fraction_level = NumericProperty()
    fraction = StringProperty()
    price = NumericProperty()
    sales_category = StringProperty()

    def __init__(self, **kwargs):
        super(BudgetItem, self).__init__(**kwargs)
        self.register_event_type('on_delete_item')

    def delete_item(self):
        budget_layout = self.parent
        budget_layout.remove_widget(self)
        self.dispatch('on_delete_item')

    def on_delete_item(self):
        pass

    def to_tuple(self):
        ''' Return a tuple with this form:
        (local_code, quantity, unit_price, sales_category, product, fraction)
        '''
        return (
            self.local_code,
            self.quantity,
            self.price,
            self.sales_category,
            self.product,
            self.fraction_level,
        )

    # def build(self):
    #     logging.debug("build")
    #     self.ids.lbl_unit_price.text = format_numeric_economy(self.price, True)
    #     # self.ids.lbl_total_quantity.text = f"{self.quantity} X {self.fraction}"
    #     self.ids.lbl_total_price.text = format_numeric_economy(self.quantity * self.unit_price, True)

    # def total_quantity(self):
    #     return f'{self.quantity} X {self.fraction}'

    # def unit_price(self):
    #     return format_numeric_economy(self.unit_price, True)

    # def total_price(self):
    #     return format_numeric_economy(self.quantity * self.unit_price, True)
