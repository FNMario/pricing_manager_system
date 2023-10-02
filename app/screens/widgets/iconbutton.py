from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.lang.builder import Builder

Builder.load_file('screens/widgets/iconbutton.kv')


class IconButton(ButtonBehavior, Image):
    pass
