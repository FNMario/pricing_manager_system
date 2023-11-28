from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty, NumericProperty, StringProperty
from kivy.lang.builder import Builder

Builder.load_file('screens/widgets/checkboxwithtext.kv')


class CheckboxWithText(Widget):
    text = StringProperty("")
    active = BooleanProperty(False)
    group = BooleanProperty(False)
    font_size = NumericProperty(18)

    def __init__(self, **kwargs):
        super(CheckboxWithText, self).__init__(**kwargs)
        self.register_event_type('on_state')

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.active = not self.active
            self.dispatch('on_state')

    def change_state(self):
        if self.children[0].children[1].state == 'normal':
            self.active = False

    def on_state(self):
        pass
