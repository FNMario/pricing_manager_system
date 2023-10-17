from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.screenmanager import NoTransition
from kivy.lang import Builder

from screens.buy import Buy
from screens.manage_prices import ManagePrices

import logging

Builder.load_file('screens/home_screen.kv')


class HomeWindow(Screen):
    id = "home_screen"
    name = "home"
    maximized = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
                self.ids.btn_manage_prices.dispatch('on_press')
                return True
            elif text == '4' or keycode == 92 and 'numlock' in modifiers:
                self.ids.btn_print_tables.dispatch('on_press')
                return True
            elif text == '5' or keycode == 93 and 'numlock' in modifiers:
                self.ids.btn_settings.dispatch('on_press')
                return True

    # Categories

    def change_category(self, instance):
        if instance.active:
            instance.active = False
            self.ids.home_screen_manager.current = "none"
        else:
            for child in self.ids.categories_layout.children:
                child.active = False
            instance.active = True
            self.ids.home_screen_manager.current = instance.screen_name

    def log_out(self):
        Window.unbind(on_key_down=self.on_key_down_home)
        for child in self.ids.categories_layout.children:
            child.active = False
        self.ids.home_screen_manager.current = "none"
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
