# from kivy.app import App
# from kivy.uix.screenmanager import ScreenManager, Screen
# from kivy.lang import Builder
# from kivy.uix.boxlayout import BoxLayout
# from screens.widgets import DoubleClickLabel, DataTable
# from screens import LoginWindow, HomeWindow, Budget, ManagePrices
from screens.home import HomeApp
from screens.login import LoginApp


# Builder.load_string("""""")

# class MyApp(App):
#     def build(self):
#         # Create a ScreenManager
#         sm = ScreenManager()

#         # Create and add the login and home screens to the ScreenManager
        
#         login_screen = Screen(name="login")
#         login_screen.add_widget(LoginWindow())
#         sm.add_widget(login_screen)

#         home_screen = Screen(name="home")
#         home_screen.add_widget(HomeWindow())
#         sm.add_widget(home_screen)

#         return sm

#     def switch_to_home_screen(self):
#         # This method will be called when the login is successful
#         self.root.current = "home"

if __name__ == '__main__':
    login = LoginApp()
    login.run()
    
    home = HomeApp()
    home.run()