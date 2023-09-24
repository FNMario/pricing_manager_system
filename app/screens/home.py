from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window, WindowBase
from kivy.uix.screenmanager import FadeTransition

import logging

from manage_prices import ManagePrices
from budgets import Budget

class HomeWindow(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.main_screen.transition = FadeTransition()

    def change_category(self,instance):
        if instance.active:
            instance.active = False
            self.ids.main_screen.current = "none"
        else:           
            for child in self.ids.categories_layout.children:
                child.active = False
            instance.active = True
            self.ids.main_screen.current = instance.screen_name
    
    def minimize(self):
        WindowBase.minimize(self)

    def maximize(self):
        WindowBase.maximize(self)

class HomeApp(App):
    def build(self):
        Window.clearcolor = (.13, .14, .19, 1)
        return HomeWindow()


if __name__ == '__main__':
    app = HomeApp()
    app.kv_file = 'home_screen.kv'
    app.run()

