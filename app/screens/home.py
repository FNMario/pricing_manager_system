import weakref
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.screenmanager import NoTransition
from kivy.lang import Builder
from screens.widgets.tabbutton import TabButton

from screens.buy import Buy
from screens.budgets import Budgets
from screens.clients import Clients
from screens.group_raise import GroupRaise
from screens.manage_prices import ManagePrices
from screens.print_tables import PrintTables
from screens.settings_screen import SettingsScreen

import logging

Builder.load_file('screens/home_screen.kv')


class HomeWindow(Screen):
    id = "home_screen"
    name = "home"
    maximized = False

    def __init__(self, **kwargs):
        super(HomeWindow, self).__init__(**kwargs)
        self.ids.home_screen_manager.transition = NoTransition()
        Window.bind(on_key_down=self.on_key_down_home)

    def on_key_down_home(self, instance, keyboard, keycode, text, modifiers):
        # print(self, instance, keyboard, keycode, text, modifiers, sep='\t')
        if keycode == 41:   # Esc
            if self.get_root_window():
                self.log_out()
                return True
        if 'ctrl' in modifiers:
            if keycode == 43:   # tab
                self.ids.home_screen_manager.current = self.ids.home_screen_manager.next()
            elif text == '1' or keycode == 89 and 'numlock' in modifiers:
                self.ids.btn_buy.dispatch('on_press')
                return True
            elif text == '2' or keycode == 90 and 'numlock' in modifiers:
                self.ids.btn_budgets.dispatch('on_press')
                return True
            elif text == '3' or keycode == 91 and 'numlock' in modifiers:
                self.ids.btn_clients.dispatch('on_press')
                return True
            elif text == '4' or keycode == 92 and 'numlock' in modifiers:
                self.ids.btn_print_tables.dispatch('on_press')
                return True
            elif text == '5' or keycode == 93 and 'numlock' in modifiers:
                self.ids.btn_manage_prices.dispatch('on_press')
                return True
            elif text == '6' or keycode == 94 and 'numlock' in modifiers:
                self.ids.btn_group_raise.dispatch('on_press')
                return True
            elif text == '9' or keycode == 97 and 'numlock' in modifiers:
                self.ids.btn_settings.dispatch('on_press')
                return True

    # Tabs

    def refresh_tabs(self, permissions):
        if permissions['access_to_buy']:
            self.add_tab('tab_buy', "Buy",
                         './assets/icons/shopping_cart.png', 'buy', 2)
        if permissions['access_to_budgets']:
            self.add_tab('tab_budgets', "Budgets",
                         './assets/icons/budget_64x64.png', 'budgets', 2)
        if permissions['access_to_clients']:
            self.add_tab('tab_clients', "Clients",
                         './assets/icons/clients_64x64.png', 'clients', 2)
        if permissions['access_to_print']:
            self.add_tab('tab_print_tables', "Print tables",
                         './assets/icons/printer_64x64.png', 'print', 2)
        if permissions['access_to_manage']:
            self.add_tab('tab_manage_prices', "Manage Prices",
                         './assets/icons/price-edit_64x64.png', 'manage', 2)
        if permissions['access_to_raise']:
            self.add_tab('tab_group_raise', "Group Raise",
                         './assets/icons/surcharges.png', 'group', 2)
        if permissions['access_to_settings']:
            self.add_tab('tab_settings', "Settings",
                         './assets/icons/settings_1.png', 'settings', 1)

    def add_tab(self, id: str, text: str, icon: str, screen_name: str, pos: int):
        ly = self.ids.tabs_layout
        tab = TabButton(
            text=text,
            icon=icon,
            on_press=self.change_tab,
            screen_name=screen_name,
        )
        ly.add_widget(tab, pos)
        self.ids[id] = weakref.ref(tab)

    def remove_tabs(self):
        for id in self.ids:
            if 'tab_' in id:
                self.ids.tabs_layout.remove_widget(self.ids[id]())

    def change_tab(self, instance):
        if instance.active:
            instance.active = False
            self.ids.home_screen_manager.current = "none"
        else:
            for child in self.ids.tabs_layout.children:
                child.active = False
            instance.active = True
            self.ids.home_screen_manager.current = instance.screen_name

    def log_out(self):
        Window.unbind(on_key_down=self.on_key_down_home)
        for child in self.ids.tabs_layout.children:
            child.active = False
        self.ids.home_screen_manager.current = "none"
        self.remove_tabs()
        self.parent.current = "login"
        self.parent.get_screen("login").ids.txt_username.focus = True

    def minimize(self):
        Window.minimize()

    def maximize(self):
        if self.maximized:
            Window.restore()
        else:
            Window.maximize()
        self.maximized = not self.maximized
