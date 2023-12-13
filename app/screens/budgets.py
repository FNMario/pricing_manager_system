from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

import logging


Builder.load_file('screens/budgets_screen.kv')


class Budgets(Screen):

    def search_budget(self, return_items: bool = False):
        if return_items:
            return []

    def clear_form(self, form):
        pass

    def on_tbl_budgets_list_selected_row(self):
        pass

    def get_cuit_cuil_list(self):
        return []

    def on_tbl_budget_selected_row(self):
        pass

    def btn_save_item(self):
        pass

    def btn_save_changes_on_press(sef):
        pass

    def btn_edit_budget_on_press(sef):
        pass

    def btn_refresh_budget_on_press(sef):
        pass

    def btn_discard_changes_on_press(sef):
        pass

    def all_upper_case(self, instance, max_length: int = None):
        instance.text = instance.text.upper()
        if type(max_length) == int:
            instance.text = instance.text[:max_length]
