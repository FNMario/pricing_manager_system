from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.screenmanager import NoTransition
from kivy.lang import Builder

from screens.buy import Buy
from screens.manage_prices import ManagePrices

import logging

Builder.load_file('screens/home_screen.kv')

class HomeWindow(Widget):
    maximized = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.main_screen.transition = NoTransition()

    def change_category(self,instance):
        if instance.active:
            instance.active = False
            self.ids.main_screen.current = "none"
        else:           
            for child in self.ids.categories_layout.children:
                child.active = False
            instance.active = True
            self.ids.main_screen.current = instance.screen_name
    
    def log_out(self):
        for child in self.ids.categories_layout.children:
            child.active = False
        self.ids.main_screen.current = "none"
        self.parent.parent.parent.ids.main_screen_manager.current = "login"
    
    def minimize(self):
        Window.minimize()

    def maximize(self):
        if self.maximized:
            Window.restore()
        else:
            Window.maximize()
        self.maximized = not self.maximized

class HomeApp(App):
    def build(self):
        Window.borderless = False
        Window.clearcolor = (.13, .14, .19, 1)
        Window.size = (1200, 800)
        Window.left = Window.left - (1200-550)/2
        Window.top = Window.top - (800-400)/2
        return HomeWindow()