from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty, StringProperty
from kivy.lang.builder import Builder

Builder.load_file('screens/widgets/checkboxwithtext.kv')


class CheckboxWithText(Widget):
    text = StringProperty("")
    active = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(CheckboxWithText, self).__init__(**kwargs)
        self.register_event_type('on_state')

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.active = not self.active
            self.dispatch('on_state')

    def on_state(self):
        pass
