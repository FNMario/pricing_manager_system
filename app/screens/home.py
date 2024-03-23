import weakref
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.screenmanager import NoTransition
from kivy.lang import Builder
from interface import logout
from screens.widgets.tabbutton import TabButton

import logging

Builder.load_file('screens/home_screen.kv')


class HomeWindow(Screen):
    id = "home_screen"
    name = "home"
    maximized = False

    def __init__(self, **kwargs):
        super(HomeWindow, self).__init__(**kwargs)
        self.ids.home_screen_manager.transition = NoTransition()

    # Keyboard handling
    def on_enter(self, *args):
        """Called when this screen is displayed to the user."""
        Window.bind(on_key_down=self.on_key_down_home)

    def on_key_down_home(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 41:   # Esc
            if self.get_root_window():
                self.log_out()
                return True
        if 'ctrl' in modifiers:
            if keycode == 43:   # tab
                self.ids.home_screen_manager.current = self.ids.home_screen_manager.next()
            elif text == '1' or keycode == 89 and 'numlock' in modifiers:
                try:
                    self.ids.tab_buy.dispatch('on_press')
                except:
                    logging.error("tab: No tab in 1 position.")
                return True
            elif text == '2' or keycode == 90 and 'numlock' in modifiers:
                try:
                    self.ids.tab_budgets.dispatch('on_press')
                except:
                    logging.error("tab: No tab in 2 position.")
                return True
            elif text == '3' or keycode == 91 and 'numlock' in modifiers:
                try:
                    self.ids.tab_clients.dispatch('on_press')
                except:
                    logging.error("tab: No tab in 3 position.")
                return True
            elif text == '4' or keycode == 92 and 'numlock' in modifiers:
                try:
                    self.ids.tab_print_tables.dispatch('on_press')
                except:
                    logging.error("tab: No tab in 4 position.")
                return True
            elif text == '5' or keycode == 93 and 'numlock' in modifiers:
                try:
                    self.ids.tab_manage_prices.dispatch('on_press')
                except:
                    logging.error("tab: No tab in 5 position.")
                return True
            elif text == '6' or keycode == 94 and 'numlock' in modifiers:
                try:
                    self.ids.tab_group_raise.dispatch('on_press')
                except:
                    logging.error("tab: No tab in 6 position.")
                return True
            elif text == '9' or keycode == 97 and 'numlock' in modifiers:
                try:
                    self.ids.tab_settings.dispatch('on_press')
                except:
                    logging.error("tab: No tab in 9 position.")
                return True

    # Tabs
    def refresh_tabs(self, permissions):
        if permissions['access_to_buy']:
            from screens.buy import Buy
            self.add_tab('tab_buy', "Buy", Buy,
                         './assets/icons/shopping_cart.png', 'buy', 2)
        if permissions['access_to_budgets']:
            from screens.budgets import Budgets
            self.add_tab('tab_budgets', "Budgets", Budgets,
                         './assets/icons/budget_64x64.png', 'budgets', 2)
        if permissions['access_to_clients']:
            from screens.clients import Clients
            self.add_tab('tab_clients', "Clients", Clients,
                         './assets/icons/clients_64x64.png', 'clients', 2)
        if permissions['access_to_print']:
            from screens.print_tables import PrintTables
            self.add_tab('tab_print_tables', "Print tables", PrintTables,
                         './assets/icons/printer_64x64.png', 'print', 2)
        if permissions['access_to_manage']:
            from screens.manage_prices import ManagePrices
            self.add_tab('tab_manage_prices', "Manage Prices", ManagePrices,
                         './assets/icons/price-edit_64x64.png', 'manage', 2)
        if permissions['access_to_raise']:
            from screens.group_raise import GroupRaise
            self.add_tab('tab_group_raise', "Group Raise", GroupRaise,
                         './assets/icons/surcharges.png', 'group', 2)
        if permissions['access_to_settings']:
            from screens.settings_screen import SettingsScreen
            self.add_tab('tab_settings', "Settings", SettingsScreen,
                         './assets/icons/settings_1.png', 'settings', 1)

    def add_tab(self, id: str, text: str, screen: Screen, icon: str, screen_name: str, pos: int):
        ly = self.ids.tabs_layout
        tab = TabButton(
            text=text,
            icon=icon,
            on_press=self.change_tab,
            screen_name=screen_name,
        )
        ly.add_widget(tab, pos)
        self.ids[id] = weakref.ref(tab)
        self.ids.home_screen_manager.add_widget(screen(name=screen_name))

    def remove_tabs(self):
        ids = list(self.ids.keys())
        for id in ids:
            if 'tab_' in id:
                screen_manager = self.ids.home_screen_manager
                tab = self.ids[id]()
                screen_manager.remove_widget(
                    screen_manager.get_screen(tab.screen_name)
                )
                self.ids.tabs_layout.remove_widget(tab)
                self.ids.pop(id)

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
        logout()
        self.parent.current = "login"
        self.parent.get_screen("login").ids.txt_username.focus = True

    # Window's control buttons
    def minimize(self):
        Window.minimize()

    def maximize(self):
        if self.maximized:
            Window.restore()
        else:
            Window.maximize()
        self.maximized = not self.maximized
