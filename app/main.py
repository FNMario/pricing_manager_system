from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

from screens.home import HomeWindow
from screens.login import LoginWindow

class MainWindow(BoxLayout):

    login_window = LoginWindow()
    home_window = HomeWindow()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ids.login_screen.add_widget(self.login_window)
        self.ids.home_screen.add_widget(self.home_window)
        self.ids.login_screen.children[0].ids.txt_username.focus = True
class MainApp(App):
    def build(self):
        Window.clearcolor = (.13, .14, .19, 1)
        return MainWindow()

if __name__=='__main__':
    MainApp().run()