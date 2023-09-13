from kivy.app import App
from kivy.uix.widget import Widget
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
        return LoginWindow()


if __name__ == '__main__':
    sa = LoginApp()
    sa.run()
