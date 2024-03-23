from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from interface import logout
from kivy.uix.screenmanager import ScreenManager

from screens.home import HomeWindow
from screens.login import LoginWindow


class MainWindow(ScreenManager):

    login_window = LoginWindow()
    home_window = HomeWindow()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(self.login_window)
        self.add_widget(self.home_window)
        self.get_screen("login").ids.txt_username.focus = True


class MainApp(App):

    def build(self):
        Window.clearcolor = (.13, .14, .19, 1)
        return MainWindow()

    def on_stop(self):
        logout()


if __name__ == '__main__':
    MainApp().run()
