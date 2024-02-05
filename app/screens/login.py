from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import logging

from interface import login

Builder.load_file('screens/login_screen.kv')


class LoginWindow(Screen):
    id = "login_screen"
    name = "login"

    def btn_login_on_press(self):
        username = self.ids.txt_username
        password = self.ids.txt_password
        lbl_info = self.ids.lbl_info

        if username.text == "":
            lbl_info.text = "[color=ff6666]Neither the username nor password field can be empty.[/color]"
            username.focus = True
            return

        if password.text == "":
            lbl_info.text = "[color=ff6666]Neither the username nor password field can be empty.[/color]"
            password.focus = True
            return

        try:
            user_permissions = login(username.text, password.text)
            logging.info(f"Login: Logged in as '{username.text}'")
            lbl_info.text = ""
            username.text = ""
            password.text = ""
            self.parent.get_screen("home").refresh_tabs(user_permissions)
            self.parent.current = "home"
        except ConnectionError as e:
            logging.error("Login: Username and password do not match.")
            lbl_info.text = "[color=ff6666]Username and password do not match.[/color]"
        except Exception as e:
            logging.error(f"Login: {e}")
            lbl_info.text = f"[color=ff6666]{e}[/color]"

        password.text = ""
        username.focus = True
