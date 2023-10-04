from kivy.uix.label import Label
from kivy.properties import NumericProperty, ObjectProperty


class DoubleClickLabel(Label):
    value = NumericProperty()

    def __init__(self, **kwargs):
        super(DoubleClickLabel, self).__init__(**kwargs)
        self.register_event_type('on_double_click')
        self.click_time = 0
        self.value_string = str(self.value)
        self.bind(value=self.update_value_string)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.is_double_tap:
                self.dispatch('on_double_click')

    def update_value_string(self, *args):
        self.value_string = str(self.value)

    def on_double_click(self):
        pass
