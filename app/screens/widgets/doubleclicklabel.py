from kivy.uix.label import Label

class DoubleClickLabel(Label):
    def __init__(self, **kwargs):
        super(DoubleClickLabel, self).__init__(**kwargs)
        self.register_event_type('on_double_click')
        self.click_time = 0

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.is_double_tap:
                self.dispatch('on_double_click')

    def on_double_click(self):
        pass
