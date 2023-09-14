from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import WindowBase
from kivy.config import Config
import logging

class LoginWindow(Widget):

    def btn_login_on_press(self):
        logging.debug('btn_login pressed')
        username = self.ids.txt_username
        password = self.ids.txt_password
        lbl_info = self.ids.lbl_info

        if username.text == "" and password.text == "":
            lbl_info.text = "[color=ff6666]Username and password can not be empty.[/color]"

        elif username.text == "asd" and password.text == "asdf":
            lbl_info.text = "[color=66ff66]Logged in![/color]"
            logging.info('Logged in')

        else:
            lbl_info.text = "[color=ff6666]Username and password do not match.[/color]"

        password.text = ""
        username.focus = True


class LoginApp(App):
    def build(self):
        self.title = 'Pricing Manager'
        self.icon = '../media/media/logo_big.png'
        WindowBase.clearcolor = (.13, .14, .19, 1)
        WindowBase.borderless = True
        return LoginWindow()


if __name__ == '__main__':
    sa = LoginApp()
    sa.run()
    Config.set('graphics', 'resizable', '0')
    Config.set('graphics', 'width', '550')
    Config.set('graphics', 'height', '400')
    Config.write()