from kivy.uix.button import Button
from kivy.lang.builder import Builder

Builder.load_file('screens/widgets/emptybutton.kv')


class EmptyButton(Button):
    pass