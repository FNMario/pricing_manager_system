from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.lang.builder import Builder
from kivy.properties import StringProperty

Builder.load_file('screens/widgets/tabbutton.kv')

class TabButton(ButtonBehavior,BoxLayout):
    icon = StringProperty()
    text = StringProperty()