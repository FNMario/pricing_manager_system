from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.lang.builder import Builder
import re

Builder.load_file('screens/widgets/selectoptiondropdown.kv')


class Option(Button):
    pass


class SelectOptionDropDown(Widget):
    icon = StringProperty('')
    text = StringProperty('')
    hint_text = StringProperty('')
    options = ListProperty()
    selected_option = 0
    readonly = BooleanProperty(True)
    dropdown = None

    def __init__(self, **kwargs):
        super(SelectOptionDropDown, self).__init__(**kwargs)
        self.register_event_type('on_press')
        self.register_event_type('on_select')
        self.register_event_type('on_text_change')

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.dispatch('on_press')

    def on_press(self, *args):
        if self.options:
            self.create_dropdown(self.options)

    def create_dropdown(self, options):
        self.dropdown = DropDown()
        for option in options:
            opt = Option(text=option)
            opt.bind(on_release=lambda opt: self.dropdown.select(opt.text))
            self.dropdown.add_widget(opt)
        self.dropdown.bind(on_select=self.option_clicked)
        self.dropdown.open(self)

    def option_clicked(self, instance, option):
        self.text = option
        self.selected_option = self.options.index(option)
        self.dispatch('on_select')
        self.dropdown.dismiss()
        next = self.ids.txt_option.get_focus_next()
        if next:
            self.ids.txt_option.focus = False
            next.focus = True

    def on_select(self):
        pass

    def text_validate(self):
        if self.dropdown.children[0].children:
            self.option_clicked(
                None, self.dropdown.children[0].children[-1].text)
        else:
            self.text = ''

    def on_text_change(self):
        if self.dropdown:
            self.dropdown.dismiss()
        if not self.readonly:
            if self.text and self.ids.txt_option.focus:
                pattern = f'^{self.text.upper()}.*$'
                options = [s for s in self.options if re.match(pattern, s)]
                self.create_dropdown(options)
            else:
                if self.ids.txt_option.focus:
                    self.create_dropdown(self.options)

    def get_focus_next(self):
        return self.ids.txt_option.get_focus_next()
