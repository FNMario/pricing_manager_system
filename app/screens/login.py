from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import logging

Builder.load_file('screens/login_screen.kv')


class LoginWindow(Screen):
    id = "login_screen"
    name = "login"

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
            self.parent.current = "home"

        else:
            lbl_info.text = "[color=ff6666]Username and password do not match.[/color]"

        password.text = ""
        username.focus = True
