from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.lang.builder import Builder

Builder.load_file('screens/widgets/optionpopup.kv')


class OptionItem(BoxLayout):
    item = NumericProperty(-1)
    text = StringProperty("Option")

    def __init__(self, **kwargs):
        super(OptionItem, self).__init__(**kwargs)
        self.register_event_type('on_click')

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.dispatch('on_click')

    def on_click(self):
        pass


class OptionPopup(Popup):
    options = ListProperty()
    selected_option = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        options_list = self.ids.bl_list
        Window.bind(on_key_down=self.on_key_down_self)

        for item, option in enumerate(self.options):
            op = OptionItem(item=item, text=option)
            op.bind(on_click=self.option_pressed)
            self.height = self.height + op.height + self.ids.bl_list.spacing
            options_list.add_widget(op)

    def option_pressed(self, option):
        self.selected_option = option.item
        self.dismiss()

    def on_key_down_self(self, instance, keyboard, keycode, text, modifiers):

        if keyboard > 48 and keyboard < 58:
            number_key = keyboard - 49
        elif keyboard > 256 and keyboard < 266 and 'numlock' in modifiers:
            number_key = keyboard - 257
        else:
            number_key = None

        if keyboard == 41:   # ESC
            self.dismiss()
        elif number_key in range(len(self.options)):
            self.selected_option = number_key
            self.dismiss()

        return True

    def on_dismiss(self):
        Window.unbind(on_key_down=self.on_key_down_self)
