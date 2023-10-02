from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.lang import Builder
import logging

Builder.load_file('screens/login_screen.kv')
class LoginWindow(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def btn_login_on_press(self):
        logging.debug('btn_login pressed')
        username = self.ids.txt_username
        password = self.ids.txt_password
        lbl_info = self.ids.lbl_info

        if username.text == "" and password.text == "":
            lbl_info.text = "[color=ff6666]Username and password can not be empty.[/color]"

        elif username.text == "asd" and password.text == "asdf":
            # lbl_info.text = "[color=66ff66]Logged in![/color]"
            lbl_info.text = ""
            username.text = ""
            logging.info('Logged in')
            self.parent.parent.parent.ids.main_screen_manager.current = "home"

        else:
            lbl_info.text = "[color=ff6666]Username and password do not match.[/color]"

        password.text = ""
        username.focus = True


class LoginApp(App):

    def build(self):
        self.title = 'Pricing Manager'
        self.icon = './assets/images/logo_big.png'
        Window.clearcolor = (.13, .14, .19, 1)
        Window.borderless = True
        Window.size = (550, 400)
        Window.left = Window.left + (1200-550)/2
        Window.top = Window.top + (800-400)/2
        return LoginWindow()


if __name__ == '__main__':
    app = LoginApp()
    app.run()