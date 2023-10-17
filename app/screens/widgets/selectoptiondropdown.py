from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.properties import StringProperty, ListProperty
from kivy.lang.builder import Builder

Builder.load_file('screens/widgets/selectoptiondropdown.kv')


class Option(Button):
    pass


class SelectOptionDropDown(Widget):
    icon = StringProperty('')
    text = StringProperty('')
    options = ListProperty()
    selected_option = 0

    def __init__(self, **kwargs):
        super(SelectOptionDropDown, self).__init__(**kwargs)
        self.register_event_type('on_press')
        self.register_event_type('on_change')

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.dispatch('on_press')

    def on_press(self):

        if self.options:
            dropdown = DropDown()
            for option in self.options:
                opt = Option(text=option)
                opt.bind(on_release=lambda opt: dropdown.select(opt.text))
                dropdown.add_widget(opt)
            dropdown.bind(on_select=self.option_clicked)
            dropdown.open(self)

    def option_clicked(self, instance, option):
        self.text = option
        self.selected_option = self.options.index(option)
        self.dispatch('on_change')

    def on_change(self):
        pass
