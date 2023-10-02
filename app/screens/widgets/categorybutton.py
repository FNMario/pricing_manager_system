from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.lang.builder import Builder

Builder.load_file('screens/widgets/categorybutton.kv')

class CategoryButton(ButtonBehavior,BoxLayout):
    pass