from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ListProperty, ObjectProperty
from screens.buy import BudgetItem
from screens.widgets.textfield import TextField
from screens.widgets.messagebox import MessageBox
from KivyCalendar import DatePicker

from interface import get_budget_items, get_budgets, get_client, get_clients, get_product_prices, save_budget

import logging


Builder.load_file('screens/budgets_screen.kv')


class Budgets(Screen):
    budget_changed = BooleanProperty(False)
    is_budget = BooleanProperty(False)
    budgets = ListProperty()
    budget_items = ListProperty()

    def show_calendar(self, instance):
        datePicker = CustomDatePicker(field=instance)
        datePicker.show_popup(1, 1)

    def search_budget(self, return_items: bool = False):
        self.budgets = get_budgets(
            budget_number=self.ids.txt_budget_number.text,
            name=self.ids.txt_search_name.text,
            from_date=self.ids.txt_from_date.text,
            to_date=self.ids.txt_to_date.text
        )
        table_budgets = [(budget[0], budget[1], budget[2])
                         for budget in self.budgets]
        if return_items:
            return table_budgets
        else:
            self.ids.tbl_budgets_list.items = table_budgets

    def clear_form(self, form):
        for field in form.children:
            if isinstance(field, TextField):
                for widget in field.children:
                    if isinstance(widget, TextInput):
                        widget.text = ""

    def on_tbl_budgets_list_selected_row(self):
        selected_row = self.ids.tbl_budgets_list.selected_row
        budget = self.budgets[selected_row]
        budget = {
            'cuit_cuil': budget[7],
            'name': budget[1],
            'phone': budget[3],
            'email': budget[4],
            'address': budget[5],
            'budget_number': budget[0]
        }
        selected_budget = int(budget['budget_number'])
        items = get_budget_items(budget_number=selected_budget)
        self.update_budget(budget_data=budget,
                           items=items)
        self.is_budget = True
        self.budget_changed = False

    def get_cuit_cuil_list(self):
        clients = get_clients()
        cuit_cuil = [client[0] for client in clients]
        return cuit_cuil

    def clear_budget(self):
        self.clear_form(self.ids.lyt_form_edit_header)
        self.ids.txt_cuit_cuil.text = ""
        self.ids.txt_name.hint_text = "Name"
        self.ids.txt_phone.hint_text = "Phone"
        self.ids.txt_email.hint_text = "Email"
        self.ids.txt_address.hint_text = "Address"
        self.ids.tbl_budget.items = []
        self.clear_form(self.ids.lyt_edit_item_form)

    def update_budget(self, budget_data: dict, items: list):
        self.clear_budget()
        # Header
        fields = {
            'budget_number': self.ids.txt_budget,
            'name': self.ids.txt_name,
            'phone': self.ids.txt_phone,
            'email': self.ids.txt_email,
            'address': self.ids.txt_address
        }
        cuit_cuil = budget_data['cuit_cuil']
        if cuit_cuil:
            self.ids.txt_cuit_cuil.text = '-'.join(
                [cuit_cuil[:2], cuit_cuil[2:10], cuit_cuil[10]])
            client = get_client(cuit_cuil)[0]
            client = {
                'name': client[1],
                'phone': client[3],
                'email': client[2],
                'address': f"{client[6]}, {client[5]}, ({client[4]})"
            }
            for field in fields:
                try:
                    fields[field].hint_text = str(client[field])
                except KeyError:
                    pass
                fields[field].text = str(budget_data[field])
        else:
            for field in fields:
                fields[field].text = str(budget_data[field])

        # Items
        # product_id, quantity, unit_price, sales_category_id, description, fraction_level
        self.budget_items = items
        # Quantity, Code, Product, Category, Unit price, Price
        table_items = [(
            str(item[1]),
            str(item[0]),
            str(item[4]),
            str(item[3]),
            str(item[2]),
            str(item[1] * item[2])
        ) for item in items]
        self.ids.tbl_budget.items = table_items

    def on_cuit_cuil_selected(self, cuit_cuil: str):
        self.clear_form(self.ids.lyt_form_edit_header)
        client = get_client(cuit_cuil)[0]
        self.ids.txt_name.hint_text = client[1]
        self.ids.txt_phone.hint_text = client[3]
        self.ids.txt_email.hint_text = client[2]
        address = f"{client[6]}" if client[6] else ""
        address += ", " if client[5] and client[6] else ""
        address += f"{client[5]}" if client[5] else ""
        address += f" ({client[4]})" if client[4] else ""
        self.ids.txt_address.hint_text = address

    def on_tbl_budget_selected_row(self, table):
        selected_row = table.selected_row
        if selected_row not in range(table._row):
            return
        item = table.items[selected_row]
        self.ids.txt_quantity.text = item[0]
        self.ids.txt_product.text = item[2]
        self.ids.optxt_category.text = item[3]
        self.ids.txt_unit_price.text = item[4]
        self.ids.txt_total_price.text = item[5]

    def _float(self, number: str) -> float:
        try:
            return float(number)
        except:
            return 0

    def on_txt_quantity_change(self):
        quantity = self._float(self.ids.txt_quantity.text)
        unit_price = self._float(self.ids.txt_unit_price.text)
        self.ids.txt_total_price.text = str(round(quantity * unit_price, 2))

    def on_txt_unit_price_change(self):
        quantity = self._float(self.ids.txt_quantity.text)
        unit_price = self._float(self.ids.txt_unit_price.text)
        self.ids.txt_total_price.text = str(round(quantity * unit_price, 2))

    def on_txt_total_price_change(self):
        def answer_clicked(answer):
            if answer == "Quantity":
                unit_price = self._float(self.ids.txt_unit_price.text)
                total_price = self._float(self.ids.txt_total_price.text)
                if unit_price == 0:
                    return
                self.ids.txt_quantity.text = str(
                    round(total_price / unit_price, 2))
            elif answer == "Unit Price":
                quantity = self._float(self.ids.txt_quantity.text)
                total_price = self._float(self.ids.txt_total_price.text)
                if quantity == 0:
                    return
                self.ids.txt_unit_price.text = str(
                    round(total_price / quantity, 2))
            else:
                return

        msg = MessageBox(
            message=f"What do you want to change?",
            kind='question',
            buttons=["Quantity", "Unit Price"],
            on_close=answer_clicked
        )

    def btn_save_item(self):
        table = self.ids.tbl_budget
        selected_row = table.selected_row
        if selected_row not in range(len(table.items)):
            return

        budget_item = self.budget_items[selected_row]

        table_item = (
            self.ids.txt_quantity.text,
            budget_item[0],
            self.ids.txt_product.text,
            self.ids.optxt_category.text,
            self.ids.txt_unit_price.text,
            self.ids.txt_total_price.text
        )
        item = (    # for self.budget_items
            budget_item[0],  # product_id
            float(table_item[0]),  # quantity
            float(table_item[4]),  # unit_price
            table_item[3],  # sales_category_id
            table_item[2],  # description
            int(budget_item[5]),  # fraction_level
        )

        if not all([i != '' for i in table_item]):
            logging.warning(
                "save_item_budget: Item not saved: Empty fields not allowed")
            return

        try:
            total_a = float(table_item[0]) * float(table_item[4])
            total_b = float(table_item[5])
            if abs(total_a - total_b) > 0.001:
                logging.error(
                    f"save_item_budget: Item not saved: {total_a} != {total_b}")
                return
        except:
            return

        table.items[selected_row] = table_item
        self.budget_items[selected_row] = item
        self.budget_changed = True
        self.clear_form(self.ids.lyt_edit_item_form)

    def btn_save_changes_on_press(self):
        budget_number = self.ids.txt_budget.text
        budget = {
            'cuit_cuil': self.ids.txt_cuit_cuil.text.replace('-', ''),
            'name': self.ids.txt_name.text,
            'phone': self.ids.txt_phone.text,
            'email': self.ids.txt_email.text,
            'address': self.ids.txt_address.text,
            'budget_number': int(budget_number) if budget_number else 0
        }
        if not (len(budget['cuit_cuil']) == 11 or budget['name']):
            MessageBox(
                message="Can't save budget. There must be a cuit/cuil or a name for the budget",
                kind='warning',
                title="Can't save budget",
                buttons='ok_only'
            )
            return
        items = self.budget_items
        try:
            save_budget(budget_data=budget, items=items)
            self.clear_budget()
            self.is_budget = False
            self.budget_changed = False
            self.search_budget()
        except Exception as e:
            logging.error(f'Budget: {e}')

    def btn_edit_budget_on_press(self):
        buy_screen = self.parent.get_screen('buy')
        def send_budget_to_buy_screen():
            # header
            name = self.ids.txt_name.text.title()
            name = name if name else self.ids.txt_name.hint_text
            budget_number = self.ids.txt_budget.text
            budget_number = budget_number if budget_number else "New budget"
            budget_name = f"{budget_number} - {name}"
            buy_screen.ids.lbl_budget_title.text = budget_name
            # items
            for item in self.budget_items:
                prices, quantities, date = get_product_prices(item[0])
                item = BudgetItem(
                    product=item[4],
                    local_code=item[0],
                    quantity=float(item[1]),
                    fraction_level=int(item[5]),
                    fraction=quantities[item[5]],
                    price=float(item[2]),
                    sales_category=item[3]
                )
                item.bind(on_delete_item=buy_screen.update_budget_total)
                buy_screen.ids.budget_layout.add_widget(item, 2)

            buy_screen.update_budget_total()
            # go to budgets_screen
            self.get_parent_window(
            ).children[-1].current_screen.ids.tab_buy.dispatch('on_press')
        is_budget = len(buy_screen.ids.budget_layout.children) > 2
        if is_budget:
            def answer_clicked(answer):
                if answer == "Cancel":
                    return
                else:
                    buy_screen.btn_discard_budget_on_press()
                send_budget_to_buy_screen()

            msg = MessageBox(
                message="There are already products in the buy tab, if you continue they will be overwritten. Do you wish to continue?",
                kind='warning',
                buttons=["Continue", "Cancel"],
                on_close=answer_clicked
            )
        else:
            send_budget_to_buy_screen()

    def btn_refresh_budget_on_press(self):

        for row, item in enumerate(self.budget_items):
            categories = {"V": 0, "D": 1, "M": 2}
            prices, _, _ = get_product_prices(item[0])
            # prices[fraction][category]
            unit_price = prices[item[5]][categories[item[3]]]
            self.budget_items[row] = (
                item[0],
                item[1],
                unit_price,
                item[3],
                item[4],
                item[5]
            )

        table_items = [(
            str(item[1]),
            str(item[0]),
            str(item[4]),
            str(item[3]),
            str(item[2]),
            str(item[1] * item[2])
        ) for item in self.budget_items]
        self.ids.tbl_budget.items = table_items

        self.budget_changed = True
        self.ids.txt_budget.text = ""    # new budget

    def btn_discard_changes_on_press(self):
        def answer_clicked(answer):
            if answer == "Cancel":
                return
            try:
                selected_budget = int(self.ids.txt_budget.text)
                budget = [item for item in self.budgets if item[0]
                          == selected_budget][0]
                budget = {
                    'cuit_cuil': budget[7],
                    'name': budget[1],
                    'phone': budget[3],
                    'email': budget[4],
                    'address': budget[5],
                    'budget_number': budget[0]
                }
                self.update_budget(budget_data=budget,
                                   items=get_budget_items(budget_number=selected_budget))
            except IndexError:
                self.clear_budget()
                self.is_budget = False
            except ValueError:
                self.clear_budget()
                self.is_budget = False
            self.budget_changed = False

        msg = MessageBox(
            message=f"Are you sure you want to discard changes?",
            kind='question',
            buttons=["Discard", "Cancel"],
            on_close=answer_clicked
        )

    def all_upper_case(self, instance, max_length: int = None):
        instance.text = instance.text.upper()
        if type(max_length) == int:
            instance.text = instance.text[:max_length]


class CustomDatePicker(DatePicker):
    field = ObjectProperty()

    def update_value(self, inst):
        """ Update textinput value on popup close """
        self.text = "%s/%s/%s" % tuple(self.cal.active_date)
        self.focus = False
        self.field.text = self.text
